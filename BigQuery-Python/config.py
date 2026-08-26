# config.py
import os
import secrets

class Config:
    # Generate a cryptographically secure secret key from environment variable
    # or create a new one if not set. In production, always use environment variables.
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    GOOGLE_APPLICATION_CREDENTIALS = "path/to/your/service-account-file.json"
    SCHEMA_PATH = "schema.xml"
    USERS = {
        "customer": {"password": "customer123", "role": "customer"},
        "admin": {"password": "admin123", "role": "admin"}
    }
