#!/usr/bin/python3
#from __future__ import print_function
"""
  Use Google admin api to update a users CAP Unit.
  #> ./setUnit.py member@nhwg.cap.gov nnn

  History:
  29Mar17 MEG Created.
"""
import httplib2
import json
import os, sys
from credentials import *

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
        orgs['department'] = sys.argv[2]
        BODY['organizations'].append( orgs )
    except KeyError:
        BODY['organizations'].append( {'primary' : 'true',
                                         'customType' : "",
                                         'department' : sys.argv[2],
                                         'description' : "" })

    if DEBUG:
        print('BODY:', BODY)

# Update user
    try:
        r = SERVICE.users().update(userKey=sys.argv[1], body=BODY).execute()
    except HttpError as e:
        print('Update failed', e)
        exit(1)


if __name__ == '__main__':
    main()

    
