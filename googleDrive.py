from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os

from googleapiclient.http import MediaFileUpload

# Define the required Google Drive scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_user_credentials():
    """Get user credentials, either from a saved token or via the OAuth flow."""
    creds = None

    # Check if the user already has a saved token
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, start the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)  # Opens a browser for login

        # Save the credentials for next time
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def upload_file_to_drive(file_path, file_name):
    """Upload a file to the user's Google Drive."""
    creds = get_user_credentials()
    service = build('drive', 'v3', credentials=creds)

    # Metadata for the file
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, resumable=True)

    # Upload the file
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File uploaded successfully. File ID: {file.get('id')}")
    return file.get('id')

if __name__ == "__main__":
    # First, authenticate the user and save their credentials
    file_id = upload_file_to_drive("example.txt", "example.txt")
