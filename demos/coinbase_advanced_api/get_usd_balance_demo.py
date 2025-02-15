from demos.auth import creds
from coinbase_advanced_trader import EnhancedRESTClient

if __name__ == '__main__':
    creds = creds.decrypt_creds()
    coinbase_rest_client = EnhancedRESTClient(creds['ca_api_key'], creds['ca_secret'])
    usd_balance = coinbase_rest_client.get_crypto_balance('USD')
    print(f"USD balance: {usd_balance}")
    usdc_balance = coinbase_rest_client.get_crypto_balance('USDC')
    print(f"USDC balance: {usdc_balance}")

