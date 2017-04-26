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
    """
    Remove a user by CAPID
    Creates a Google Admin SDK API service object and deletes
    user info for CAPID specified as argv[1]
    """
    try:
        DEBUG = os.environ['DEBUG']
    except:
        DEBUG = 0

    CREDENTIALS = get_credentials()
    HTTP = CREDENTIALS.authorize(httplib2.Http())
    SERVICE = discovery.build('admin', 'directory_v1', http=HTTP)

    try:
        result = SERVICE.users().list(domain='nhwg.cap.gov',
                                      maxResults=1,
                                      query='externalId:'+sys.argv[1]).execute()
    except HttpError as e:
        print('CAPID not found!', e)
        exit(1)

    # extract member object from result users array and get primary email

    try:
        member = result['users'][0]
        primaryEmail = member['primaryEmail']
    except KeyError as e:
        print('Error: Member ' + sys.argv[1] + ' not found.')
        exit(1)
    
    try:
        result = SERVICE.users().delete( userKey=primaryEmail ).execute()
    except HttpError as e:
        print('Error:', e)
        exit(1)


if __name__ == '__main__':
    main()
