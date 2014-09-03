#!/usr/bin/python
'''
google drive API
open a service for development
https://console.developers.google.com/project

document for python
https://developers.google.com/drive/web/quickstart/quickstart-python
'''

#Copy a document to google drive.
import httplib2
import pprint

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

from oauth2client.file import Storage
from oauth2client.util import logger


# Copy your credentials from the console
CLIENT_ID = '<INPUT CLIENT ID>'
CLIENT_SECRET = '<INPUT CLIENT SECRET ID>'

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# Path to the file to upload
FILENAME = 'document.txt'

code = ''

# Run through the OAuth flow and retrieve credentials
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)

# if OAuth file are existed ?
storage = Storage('OAuthCredentials.txt')
credentials = storage.get()

if credentials is None:
    # Authorization Step 1
    authorize_url = flow.step1_get_authorize_url()
    print 'Go to the following link in your browser: ' + authorize_url
    code = raw_input('Enter verification code: ').strip()
    # Authorization Step 2
    credentials = flow.step2_exchange(code)
else:
    code = credentials

# store to local file
storage.put(credentials)

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

drive_service = build('drive', 'v2', http=http)

# Insert a file
media_body = MediaFileUpload(FILENAME, mimetype='text/plain', resumable=True)
body = {
  'title': 'InsertTest1',
  'description': 'A test document',
  'mimeType': 'text/plain'
}

file = drive_service.files().insert(body=body, media_body=media_body).execute()
pprint.pprint(file)
