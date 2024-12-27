from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def list_files():
    """List files in Google Drive."""
    # Load service account credentials
    credentials = service_account.Credentials.from_service_account_file(
        'lastnote-446010-76bf6183b299.json'
    )

    try:
        # Create Drive API client
        service = build("drive", "v3", credentials=credentials)

        # List files
        results = service.files().list(
            pageSize=10,  # Number of files to retrieve
            fields="nextPageToken, files(id, name)"
        ).execute()

        items = results.get('files', [])

        if not items:
            print("No files found.")
        else:
            print("Files:")
            for item in items:
                print(f"Name: {item['name']}, ID: {item['id']}")

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    list_files()
