# DUDE BEFORE U MUST CREATE FOLLOWING::
# 1. create a project
# 2. create oAuth client, get credentials
# 3. Enable google drive for that project.
# 4. run this file>> this will save the credentials in token.pickle...
#


from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata']
SCOPES = ['https://www.googleapis.com/auth/drive']


def authUser():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        print("\n\nAlready authorized..")
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        print("\n\nNot Authorized..")
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("\n\nCreds expired..")
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            print("\n\nSaving creds...")
            pickle.dump(creds, token)

authUser()