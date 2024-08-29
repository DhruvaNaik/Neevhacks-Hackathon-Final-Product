from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from bs4 import BeautifulSoup
import ast
from algorithm import decrypt_text

# Set up the OAuth 2.0 flow
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_message_body(payload):
    """
    Recursively extract the message body from the payload, considering text/plain and text/html content types.
    """
    body = ""

    if 'parts' in payload:
        # Iterate through parts to find the body content
        for part in payload['parts']:
            body += get_message_body(part)
    else:
        # Decode the body data based on the content type
        mime_type = payload.get('mimeType')
        data = payload.get('body', {}).get('data')
        if data:
            decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
            if mime_type == 'text/plain':
                body += decoded_data
            elif mime_type == 'text/html':
                # Parse HTML content and extract text
                soup = BeautifulSoup(decoded_data, 'html.parser')
                body += soup.get_text()

    return body

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
        
        # Extract the full message body
        body = get_message_body(msg['payload'])

        # Extract necessary information
        message_info = {
            'id': msg['id'],
            'threadId': msg['threadId'],
            'subject': headers.get('Subject', '(No Subject)'),
            'from': headers.get('From', '(Unknown Sender)'),
            'date': headers.get('Date', '(No Date)'),
            'snippet': snippet,
            'body': body  # Full message body
        }

        detailed_messages.append(message_info)

    return detailed_messages

if __name__ == '__main__':
    messages = main()
    for msg in messages:
        print(f"Subject: {msg['subject']}")
        print(f"From: {msg['from']}")
        print(f"Date: {msg['date']}")
        print(f"Body: {msg['body'][:500]}...")  # Print the first 500 characters of the body
        print("\n" + "-"*80 + "\n")
        if msg['from'] == 'quantaamail@gmail.com':
            # decrypt_text_subject = ast.literal_eval(msg['subject'])
            decrypt_text_body = ast.literal_eval(msg['body'])
            try:
                print(decrypt_text(decrypt_text_body))
            except:
                print('The mail was not decrypted')
        
        




            