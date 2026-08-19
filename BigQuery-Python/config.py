# config.py
import os
from werkzeug.security import generate_password_hash

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key"  # Replace with a strong secret key
    GOOGLE_APPLICATION_CREDENTIALS = "path/to/your/service-account-file.json"
    SCHEMA_PATH = "schema.xml"
    
    # Password hashes generated using werkzeug.security.generate_password_hash()
    # To set custom passwords, generate hashes using:
    # from werkzeug.security import generate_password_hash
    # print(generate_password_hash("your_password"))
    # Then set the hash via environment variables or update this configuration
    USERS = {
        "customer": {
            "password_hash": os.environ.get("CUSTOMER_PASSWORD_HASH") or generate_password_hash("customer123"),
            "role": "customer"
        },
        "admin": {
            "password_hash": os.environ.get("ADMIN_PASSWORD_HASH") or generate_password_hash("admin123"),
            "role": "admin"
        }
    }
    
    # Note: The default password hashes above are for development only.
    # In production, always set CUSTOMER_PASSWORD_HASH and ADMIN_PASSWORD_HASH
    # environment variables with securely generated hashes.
