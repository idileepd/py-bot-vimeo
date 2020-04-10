from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import socket
# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES = ['https://www.googleapis.com/auth/drive']

# SCOPES = ['https://www.googleapis.com/auth/drive.metadata', 'https://www.googleapis.com/auth/drive']

creds = None
socket.setdefaulttimeout(600)  # set timeout to 10 minutes
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
       creds = pickle.load(token)
else:
    print("NO TOKEN >>> :(")

service = build('drive', 'v3', credentials=creds)

def get_files():
    # Call the Drive v3 API
    results = service.files().list( pageSize=10, fields="nextPageToken, files(id, name)").execute() # pylint: disable=maybe-no-member
    
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

# get_files()


def upload_photo():
    print("Uploading photo..")
    file_metadata = {'name': 'photo.jpg'}
    media = MediaFileUpload('photo.jpg',mimetype='image/jpeg')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute() # pylint: disable=maybe-no-member
    print('File ID: %s' % file.get('id'))

# upload_photo()

def upload_photo_to_folder(folder_id):
    print("Uploading photo..")
    folder_id = folder_id
    file_metadata = {
    'name': 'photo.jpg',
    'parents': [folder_id]
    }
    media = MediaFileUpload('photo.jpg',mimetype='image/jpeg')
    file = service.files().create(body=file_metadata, media_body=media,).execute() # pylint: disable=maybe-no-member
    print('File ID: %s' % file.get('id'))
    print(file)

# upload_photo_to_folder('1bGZMvAHexIMZ8FRFEFWeB3Qucg9j0hDq')

def upload_video_to_folder(folder_id):
    print("Uploading photo..")
    folder_id = folder_id
    file_metadata = {
    'name': 'test.mp4',
    'parents': [folder_id]
    }
    media = MediaFileUpload('test.mp4',mimetype='video/mp4')
    file = service.files().create(body=file_metadata, media_body=media,).execute() # pylint: disable=maybe-no-member
    print('File ID: %s' % file.get('id'))
    print(file)

upload_video_to_folder('1bGZMvAHexIMZ8FRFEFWeB3Qucg9j0hDq')
