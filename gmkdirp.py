#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Explanation:

This script is a general publisher of content to a Google Drive.

Designed to work with an Oauth token, please refer to documents
on how to set up a token and use specific SCOPES

Usage:
    $ python  gmkdirp [ options ]

Style:
    Google Python Style Guide:
    http://google.github.io/styleguide/pyguide.html

    @name           gmkdirp
    @version        1.0.0
    @author-name    Wayne Schmidt
    @author-email   wayne.kirk.schmidt@gmail.com
    @license-name   GNU GPL
    @license-url    http://www.gnu.org/licenses/gpl.html
"""

__version__ = '1.0.0'
__author__ = "Wayne Schmidt (wayne.kirk.schmidt@gmail.com)"

import argparse
import datetime
import re
import sys
import os
import pickle
import apiclient
import google
import googleapiclient
import google_auth_oauthlib

sys.dont_write_bytecode = 1

PARSER = argparse.ArgumentParser(description="""
A multi output publisher for documents to a Google drive.
""")

PARSER.add_argument('-c', metavar='<creds>', dest='creds', help='specify secret file')
PARSER.add_argument('-t', metavar='<token>', dest='token', help='specify token file')
PARSER.add_argument('-d', metavar='<dir>', dest='dir', help='specify target directory')
PARSER.add_argument('-p', metavar='<parent>', dest='parent', help='specify parent directory')
PARSER.add_argument('-v', '--verbose', help='verbose', action="store_true")

ARGS = PARSER.parse_args()

CURRENT = datetime.datetime.now()
DSTAMP = CURRENT.strftime("%Y%m%d")
TSTAMP = CURRENT.strftime("%H%M%S")
LSTAMP = DSTAMP + '.' + TSTAMP

if ARGS.creds:
    os.environ['CREDENTIALS'] = ARGS.creds
if ARGS.token:
    os.environ['TOKENFILE'] = ARGS.token
if ARGS.dir:
    os.environ['TARGETDIR'] = ARGS.dir

try:
    CREDENTIALS = os.environ['CREDENTIALS']
    TOKENFILE = os.environ['TOKENFILE']
    TARGETDIR = os.environ['TARGETDIR']

except KeyError as myerror:
    print('Environment Variable Not Set :: {} '.format(myerror.args[0]))

SCOPES = ('https://www.googleapis.com/auth/drive')

def create_auth():
    """
    Fetch or create the credentials used to create the service
    """
    if os.path.exists(TOKENFILE):
        with open(TOKENFILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKENFILE, 'wb') as token:
            pickle.dump(creds, token)
    service = googleapiclient.discovery.build('drive', 'v3', credentials=creds)

    return service

def create_target_dir(service, pathname, parentid):
    """
    Create the target directory to store the files
    """
    dir_metadata = {
        'name': pathname,
        'parents' : [parentid],
        'mimeType': 'application/vnd.google-apps.folder'
    }
    child = service.files().create(body=dir_metadata, \
                                      fields='id,name,parents').execute()
    my_name = child['name']
    my_id = child['id']
    my_parent = child['parents'][0]

    if ARGS.verbose:
        print('Folder_ID: %s' % my_id)
        print('Folder_Name: %s' % my_name)
        print('Folder_Parent_ID: %s' % my_parent)

    return (my_name, my_id, my_parent)

def calculate_parent(service, parentname):
    """
    Calculate or search for base directory
    """
    if parentname == 'myrootdrive':
        file_metadata = {
            'name': parentname + LSTAMP,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        temp_id = service.files().create(body=file_metadata, \
                                              fields='id').execute()["id"]
        my_drive_id = service.files().get(fileId=temp_id, \
                                        fields='parents').execute()["parents"][0]
        service.files().delete(fileId=temp_id).execute()

        my_name = 'mydrive'
        my_id = my_drive_id
        my_parent = my_drive_id

    else:
        children = service.files().list(q="mimeType='application/vnd.google-apps.folder' \
                                        and name='"+parentname+"'", spaces='drive', \
                                        fields='nextPageToken, \
                                        files(id, name, parents)').execute()
        for child in children['files']:
            my_name = child['name']
            my_id = child['id']
            my_parent = child['parents'][0]

    return (my_name, my_id, my_parent)

def split_into_path_list(target_path):
    """
    split targetpath into specifiic parts
    """
    path_delimiters = '/', '\\'
    path_regex = '|'.join(map(re.escape, path_delimiters))
    path_list = re.split(path_regex, target_path, 0)

    return path_list

def main():
    """
    This is the main lodule for authentication, and file operations
    """
    (service) = create_auth()

    path_list = list()
    parentname = 'myrootdrive'
    if ARGS.parent:
        parentname = ARGS.parent
    path_list.append(parentname)

    (base_name, base_id, base_parent_id) = calculate_parent(service, parentname)
    parent_id = base_id

    if ARGS.verbose:
        print('Beginning_ID: %s' % base_id)
        print('Beginning_Folder_Name: %s' % base_name)
        print('Beginning_Folder_Parent_ID: %s' % base_parent_id)

    for path_item in split_into_path_list(os.environ['TARGETDIR']):
        if ARGS.verbose:
            print('CURRENT_Parent_ID: %s' % parent_id)
        (_item_name, item_id, _item_parent) = create_target_dir(service, path_item, parent_id)
        parent_id = item_id

if __name__ == '__main__':
    main()
