from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Path to your JSON key file
SERVICE_ACCOUNT_FILE = 'lastnote-446010-76bf6183b299.json'

# Scopes for the Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

# Authenticate with the service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Drive API client
service = build('drive', 'v3', credentials=credentials)

def upload_file(file_path, file_name, folder_id=None):
    """
    Upload a file to Google Drive.

    Args:
        file_path (str): The local path to the file.
        file_name (str): The name the file should have on Google Drive.
        folder_id (str): The ID of the folder to upload the file to (optional).

    Returns:
        str: The ID of the uploaded file.
    """
    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    print(f"File uploaded successfully. File ID: {file.get('id')}")
    return file.get('id')


# Example: Upload a file
file_path = 'todo1.db'  # Path to the local file
file_name = 'example_uploaded.db'  # Name to be used on Google Drive
folder_id = 'lastnote'  # Replace with your Google Drive folder ID, or None for root

upload_file(file_path, file_name)
