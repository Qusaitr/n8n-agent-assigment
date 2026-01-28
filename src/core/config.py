import os
import sys
from dotenv import load_dotenv

class Config:
    """Manages system configuration and environment variables."""
    
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.google_creds_file = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
        self.google_token_file = os.getenv("GOOGLE_TOKEN_FILE", "token.json")
        self.google_scopes = os.getenv("GOOGLE_SCOPES", "https://mail.google.com/").split(",")

    def validate(self):
        """Validates critical configuration."""
        errors = []
        if not self.openai_api_key:
            errors.append("❌ OPENAI_API_KEY not found in .env")
        if not os.path.exists(self.google_creds_file):
            errors.append(f"❌ '{self.google_creds_file}' not found.")
        
        if errors:
            for err in errors:
                print(err)
            sys.exit(1)

# Singleton instance for global access
config = Config()
