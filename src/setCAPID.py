#!/usr/bin/python3
#from __future__ import print_function
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
    """Retrieve a member record from Google and update the CAPID
       argv[1] - member wing email address
       argv[2] - CAPID (nnnnnn)
    """
    try:
        DEBUG = os.environ['DEBUG']
    except:
        DEBUG = 0

# Connect to Google and authorize make a service httpRequest object
    CREDENTIALS = get_credentials()
    HTTP = CREDENTIALS.authorize(httplib2.Http())
    SERVICE = discovery.build('admin', 'directory_v1', http=HTTP)

    try:
        member = SERVICE.users().get(userKey=sys.argv[1]).execute()
    except:
        print('User not found!')
        exit(1)

    if DEBUG:
        print(member)

# Build the request body for the update 
    BODY = {}
    BODY['externalIds']=[]
    BODY['externalIds'].append( {'value' : sys.argv[2], 'type' :
                                       'organization' })

    if DEBUG:
        print('BODY:', BODY)

    try:
       r = SERVICE.users().update(userKey=sys.argv[1], body=BODY).execute()
    except:
        print('Update failed')
        exit(1)


if __name__ == '__main__':
    main()
