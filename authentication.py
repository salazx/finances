import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_user():
    """Authenticate the user and save the credentials to a file."""
    creds = None

    # Check if token.json exists
    if os.path.exists('token.json'):
        print("token.json found. Attempting to load credentials.")
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            print("Credentials are invalid or expired.")
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing credentials...")
                creds.refresh(Request())
            else:
                print("Starting new authentication flow.")
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', SCOPES)
                creds = flow.run_local_server(port=0)
                # Save the credentials for future runs
                with open('token.json', 'w') as token:
                    print("Writing token.json...")
                    token.write(creds.to_json())
    else:
        print("token.json not found. Running authentication process.")
        if os.path.exists('client_secret.json'):
            print("client_secret.json found. Starting flow...")
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                print("Writing token.json...")
                token.write(creds.to_json())
        else:
            raise FileNotFoundError("client_secret.json not found in the current directory.")
    
    return creds

def get_credentials():
    " Retrieve the user's credentials. """
    if os.path.exists('token.json'):
        print("token.json found. Attempting to load credentials.")
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        print("Credentials loaded succesfully.")
        return creds
    else:
        # if credentials don't exist, run the authentication process
        print("token.json not found. Running authentication process.")
        return authenticate_user()
