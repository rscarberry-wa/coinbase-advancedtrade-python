import os
from getpass import getpass

from demos.auth import creds
from coinbase_advanced_trader import AlphaSquared
import json

if __name__ == '__main__':
    password = os.getenv("CREDS_PW")
    if password is None:
        password = getpass("Enter your password: ")
    creds = creds.decrypt_creds(password=password)
    alphasquared = AlphaSquared(api_token=creds['as_token'])

    strategies = ['link_cons_100', 'sol_mod_100', 'eth_mod_100', 'btc_agg_100']
    for strategy in strategies:
        strategy_values = alphasquared.get_strategy_values(strategy)
        print(json.dumps(strategy_values, indent=4))
