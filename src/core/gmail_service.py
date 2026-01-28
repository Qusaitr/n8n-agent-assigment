import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from src.core.config import config

class GmailService:
    """Encapsulates Gmail API interactions."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GmailService, cls).__new__(cls)
            cls._instance._creds = None
        return cls._instance

    def get_credentials(self):
        """Handles OAuth2 authentication logic."""
        if self._creds and self._creds.valid:
            return self._creds
            
        if os.path.exists(config.google_token_file):
            self._creds = Credentials.from_authorized_user_file(
                config.google_token_file, config.google_scopes
            )
        
        if not self._creds or not self._creds.valid:
            if self._creds and self._creds.expired and self._creds.refresh_token:
                self._creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    config.google_creds_file, config.google_scopes
                )
                self._creds = flow.run_local_server(port=0)
            
            with open(config.google_token_file, 'w') as token:
                token.write(self._creds.to_json())
                
        return self._creds

    def get_service(self):
        """Returns a built Gmail service instance."""
        creds = self.get_credentials()
        return build('gmail', 'v1', credentials=creds)

# Singleton helper
gmail_service_manager = GmailService()
