import os
from getpass import getpass

from demos.auth import creds
from coinbase_advanced_trader import AlphaSquared
import json

# {
#     "id": "1",
#     "asset_id": "bitcoin",
#     "symbol": "BTC",
#     "name": "Bitcoin",
#     "current_risk": "54.00",
#     "avg_risk_30d": "58.54",
#     "current_price": "95654.49",
#     "market_cap": "1896783172867",
#     "market_cap_rank": "1",
#     "price_change_percentage_24h": "-1.33",
#     "price_change_percentage_7d_in_currency": "-2.59",
#     "price_change_percentage_14d_in_currency": "-6.28",
#     "price_change_percentage_30d_in_currency": "3.75",
#     "market_cap_change_24h": "-22850676676",
#     "market_cap_change_percentage_24h": "-1.19",
#     "circulating_supply": "19823253.00000000",
#     "total_supply": "19823253.00000000",
#     "max_supply": "21000000.00000000",
#     "ath": "108786.00",
#     "ath_change_percentage": "-11.95",
#     "last_updated": "2025-02-12 16:06:59",
#     "risk_change_percentage_7d": "-1.62",
#     "risk_change_percentage_14d": "-9.77",
#     "risk_change_percentage_30d": "-2.85",
#     "previous_risk_band": "50.00",
#     "lowest_risk_30d": "54.50",
#     "highest_risk_30d": "61.90",
#     "lowest_risk_7d": "54.50",
#     "highest_risk_7d": "55.50"
# }

if __name__ == '__main__':
    password = os.getenv("CREDS_PW")
    if password is None:
        password = getpass("Enter your password: ")
    creds = creds.decrypt_creds(password=password)
    alphasquared = AlphaSquared(api_token=creds['as_token'])
    print(json.dumps(alphasquared.get_asset_info('BTC'), indent=4))

