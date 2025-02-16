from demos.auth import creds
from alphasquared import AlphaSquared
import json

if __name__ == '__main__':
    creds = creds.decrypt_creds()
    alphasquared = AlphaSquared(api_token=creds['as_token'])

    strategies = ['link_cons_100', 'sol_mod_100', 'eth_mod_100', 'btc_agg_100']
    for strategy in strategies:
        strategy_values = alphasquared.get_strategy_values(strategy)
        print(json.dumps(strategy_values, indent=4))
