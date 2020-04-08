from __future__ import print_function
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import socket
import os


socket.setdefaulttimeout(600)  # set timeout to 10 minutes
SCOPES = ['https://www.googleapis.com/auth/drive']

my_folder_id = '16m8_vJaE--4LludRLZNSVVP86j1XrAkT'

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# conver sting paths..
BASE_DIR = '/'.join(BASE_DIR.split('\\'))
TEMP_DIR = '/'.join(TEMP_DIR.split('\\'))
OUTPUT_DIR = '/'.join(OUTPUT_DIR.split('\\'))

creds = None


print("Executing Drive.py")
print("Getting tokne.pickle")

print(f"BASE DIR :: {BASE_DIR}")
print(f"TEMP_DIR :: {TEMP_DIR}")
print(f"OUTPUT_DIR :: {OUTPUT_DIR}\n\n")



if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
       creds = pickle.load(token)
else:
    print("NO TOKEN >>> :(")

service = build('drive', 'v3', credentials=creds)


def upload_video_to_this_folder(folder_id, file_name):
    try:
        file_name = file_name+'.mp4'
        print(f"Uploading {file_name} to my_folder.. :: {folder_id}")
        file_metadata = {
        'name': file_name,
        'parents': [folder_id]
        }
        file_path = os.path.join(OUTPUT_DIR, file_name)
        file_path = '/'.join(file_path.split('\\'))
        print(f"File path : {file_path}")
        media = MediaFileUpload(file_path, mimetype='video/mp4')
        file_res = service.files().create(body=file_metadata, media_body=media,).execute() # pylint: disable=maybe-no-member
        print('File ID: %s' % file_res.get('id'))
        print(f"File upload done : {file_name} :: \n {file_res}")
        print(f"deleting file : {file_path}")
        media =None # to close connection with file
        os.remove(file_path)
        return [True, file_res]
    except:
        print(f"\n\n\n\n\n {file_name} <<<<<<< ERROR OCCURED IN UPLOAD VIDEO TO GOOGLE Drive ")
        return [False, file_name+'File failed to upload to drive']



def test_upload_video_to_this_folder(folder_id, file_name):
    file_name = file_name+'.mp4'
    print(f"Uploading {file_name} to my_folder.. :: {folder_id}")
    file_metadata = {
    'name': file_name,
    'parents': [folder_id]
    }
    file_path = os.path.join(OUTPUT_DIR, file_name)
    file_path = '/'.join(file_path.split('\\'))
    print(f"File path : {file_path}")
    media = MediaFileUpload(file_path, mimetype='video/mp4')

    file_res = service.files().create(body=file_metadata, media_body=media,).execute() # pylint: disable=maybe-no-member
    media =None # to close connection with file
    print('File ID: %s' % file_res.get('id'))
    print(f"File upload done : {file_name} :: \n {file_res}")
    print(f"deleting file : {file_path}")
    # file_res.content.close()
    os.remove(file_path)
    return [True, file_res]


# x = test_upload_video_to_this_folder(my_folder_id, 'testx')
# print(x)




def upload_video_to_my_folder(file_name):
    try:
        file_name = file_name+'.mp4'
        print(f"Uploading {file_name} to my_folder.. :: {my_folder_id}")
        file_metadata = {
        'name': file_name,
        'parents': [my_folder_id]
        }
        file_path = os.path.join(OUTPUT_DIR, file_name)
        file_path = '/'.join(file_path.split('\\'))
        print(f"File path : {file_path}")
        media = MediaFileUpload(file_path, mimetype='video/mp4')
        file_res = service.files().create(body=file_metadata, media_body=media,).execute() # pylint: disable=maybe-no-member
        print('File ID: %s' % file_res.get('id'))
        print(f"File upload done : {file_name} :: \n {file_res}")
        return [True, file_res]
    except:
        print(f"\n\n\n\n\n {file_name} <<<<<<< ERROR OCCURED IN UPLOAD VIDEO TO GOOGLE Drive ")
        return [False, file_name+'File failed to upload to drive']


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
    # file_path = "C:/Users/Venu Gopal/Desktop/py-bot/photo.jpg"
    file_metadata = {
    'name': 'photos.jpg',
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

# upload_video_to_folder('1bGZMvAHexIMZ8FRFEFWeB3Qucg9j0hDq')
