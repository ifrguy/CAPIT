#!/usr/bin/python3
#from __future__ import print_function
"""
  Use Google admin api to update a users CAP Type: SENIOR | CADET.
  #> ./setType.py member@nhwg.cap.gov (SENIOR | CADET)

  History:
  29Mar17 MEG Created.
"""
import httplib2
import json
import os, sys

from googleapiclient import discovery
from googleapiclient.errors import *
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

DEBUG=0

#try:
#    import argparse
#    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#except ImportError:
#    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/admin-directory_v1-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Directory API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'admin-directory_v1-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Retrieve a member record from Google and update the Unit
       argv[1] - member wing email address
       argv[2] - CAP Unit (nnn)
    """
    try:
        DEBUG = os.environ['DEBUG']
    except:
        DEBUG = 0

    # Authorize connection and build service request object
    CREDENTIALS = get_credentials()
    HTTP = CREDENTIALS.authorize(httplib2.Http())
    SERVICE = discovery.build('admin', 'directory_v1', http=HTTP)

    # make sure member exists before we try anything
    try:
        member = SERVICE.users().get(userKey=sys.argv[1]).execute()
    except:
        print('User not found!')
        exit(1)

    if DEBUG:
        print(member)

    BODY = {}  # create empty dict as http request body for update
    BODY['organizations'] = []

    try:
        orgs = member['organizations'][0]
        orgs['description'] = sys.argv[2]
        BODY['organizations'].append( orgs )
    except KeyError:
        BODY['organizations'].append( {'primary' : 'true',
                                         'customType' : "",
                                         'department' : "",
                                         'description' : sys.argv[2] })

    # Update user
    try:
        r = SERVICE.users().update(userKey=sys.argv[1], body=BODY).execute()
    except:
        print('Update failed')
        exit(1)


if __name__ == '__main__':
    main()

    
