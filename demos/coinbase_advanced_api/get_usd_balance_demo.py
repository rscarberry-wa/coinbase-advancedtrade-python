import os
from getpass import getpass

from demos.auth import creds
from coinbase_advanced_trader import EnhancedRESTClient
from decimal import Decimal

if __name__ == '__main__':
    password = os.getenv("CREDS_PW")
    if password is None:
        password = getpass("Enter your password: ")
    creds = creds.decrypt_creds(password=password)
    coinbase_rest_client = EnhancedRESTClient(creds['ca_api_key'], creds['ca_secret'])
    product_id = 'BTC-USDC'
    value = Decimal('400')
    currency = product_id.split('-')[1]
    currency_balance = Decimal(coinbase_rest_client.get_crypto_balance(currency))
    if currency_balance < value:
        print(f"Insufficient {currency} balance. Required: {value}, Available: {currency_balance:.2f}")
    else:
        print(f"Sufficient {currency} balance. Required: {value}, Available: {currency_balance:.2f}")


