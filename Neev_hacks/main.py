from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Set up the OAuth 2.0 flow
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    # Load the credentials from the file
    creds = None
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=8000)

    # Build the Gmail API service
    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API to fetch the list of messages
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])

    # Initialize a list to hold the detailed message information
    detailed_messages = []

    # Fetch details for each message
    for message in messages[:10]:  # Limit to the first 10 messages for now
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        headers = {header['name']: header['value'] for header in msg['payload']['headers']}
        snippet = msg.get('snippet', '')

        # Extract necessary information
        message_info = {
            'id': msg['id'],
            'threadId': msg['threadId'],
            'subject': headers.get('Subject', '(No Subject)'),
            'from': headers.get('From', '(Unknown Sender)'),
            'date': headers.get('Date', '(No Date)'),
            'snippet': snippet
        }

        detailed_messages.append(message_info)

    return detailed_messages