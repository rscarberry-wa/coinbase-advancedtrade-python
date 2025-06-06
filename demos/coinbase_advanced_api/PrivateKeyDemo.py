import os
from getpass import getpass

from cryptography.hazmat.primitives import serialization

from demos.auth import creds

if __name__ == "__main__":
    password = os.getenv("CREDS_PW")
    if password is None:
        password = getpass("Enter your password: ")
    creds = creds.decrypt_creds(password=password)
    if creds:
        secret_key = creds['ca_secret']
        private_key_bytes = secret_key.encode("utf-8")
        private_key = serialization.load_pem_private_key(
            private_key_bytes, password=None
        )
        print(private_key)
    else:
        print("Error decrypting credentials")
