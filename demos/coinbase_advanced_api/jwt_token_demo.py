import os
from getpass import getpass
import requests

from coinbase import jwt_generator
from demos.auth import creds

if __name__ == "__main__":
    password = os.getenv("CREDS_PW")
    if password is None:
        password = getpass("Enter your password: ")
    creds = creds.decrypt_creds(password=password)
    if creds:
        api_key = creds['ca_api_key']
        api_secret = creds['ca_secret']
        request_method = "GET"
        request_path = "/api/v3/brokerage/accounts"
        jwt_uri = jwt_generator.format_jwt_uri(request_method, request_path)
        jwt_token = jwt_generator.build_rest_jwt(jwt_uri, api_key, api_secret)

        headers = {"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"}
        response = requests.get(
            'https://api.coinbase.com/api/v3/brokerage/accounts', headers=headers)
        print(response.json())
    else:
        print("Error decrypting credentials.")


