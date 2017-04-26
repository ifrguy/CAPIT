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
    """Shows basic usage of the Google Admin SDK Directory API.

    Creates a Google Admin SDK API service object and outputs 
    user info for userKey specified as argv[1]
    """
    try:
        DEBUG = os.environ['DEBUG']
    except:
        DEBUG = 0


    CREDENTIALS = get_credentials()
    HTTP = CREDENTIALS.authorize(httplib2.Http())
    SERVICE = discovery.build('admin', 'directory_v1', http=HTTP)

    try:
        member = SERVICE.users().get(userKey=sys.argv[1]).execute()
    except:
        print('User: ', sys.argv[1], ' not found!')
        exit(0)

    if DEBUG:
        print(member.values())
    try:
        print('Name: ', member['name']['fullName'])
    except KeyError as e:
        print('Missing attribute key:' , e)
    try:
        print('email: ', member['primaryEmail'])
    except KeyError as e:
        print('Missing attribute key:' , e)
    try:
        print('CAPID: ', member['externalIds'][0]['value'])
    except KeyError as e:
        print('Missing attribute key:' , e)
    try:
        print('Type: ', member['organizations'][0]['description'])
    except KeyError as e:
        print('Missing attribute key:' , e)
    try:
        print('Unit: ', member['organizations'][0]['department'])
    except KeyError as e:
        print('Missing attribute key:' , e)
    try:
        print('OrgUnitPath: ', member['orgUnitPath'])
    except KeyError as e:
        print('Missing attribute key:' , e)
    try:
        print('Last Login: ', member['lastLoginTime'])
    except KeyError as e:
        print('Missing attribute key:' , e)
    try:
        print('Creation Time: ', member['creationTime'])
    except KeyError as e:
        print('Missing attribute key:' , e)
    try:
        print('Is Admin: ', member['isAdmin'])
    except KeyError as e:
        print('Missing attribute key:' , e)


if __name__ == '__main__':
    main()

    
