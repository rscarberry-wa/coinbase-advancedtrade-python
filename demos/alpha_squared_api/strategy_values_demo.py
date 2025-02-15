from demos.auth import creds
from alphasquared import AlphaSquared
import json

# {
#     "strategy_name": "btc_agg_100",
#     "buy_values": {
#         "risk_0": "160",
#         "risk_5": "160",
#         "risk_10": "160",
#         "risk_15": "140",
#         "risk_20": "140",
#         "risk_25": "120",
#         "risk_30": "120",
#         "risk_35": "100",
#         "risk_40": "100",
#         "risk_45": "80",
#         "risk_50": "80",
#         "risk_55": "60",
#         "risk_60": "60",
#         "risk_65": "40",
#         "risk_70": "40",
#         "risk_75": "0",
#         "risk_80": "",
#         "risk_85": "",
#         "risk_90": "",
#         "risk_95": "",
#         "risk_100": ""
#     },
#     "sell_values": {
#         "risk_0": "",
#         "risk_5": "",
#         "risk_10": "",
#         "risk_15": "",
#         "risk_20": "",
#         "risk_25": "",
#         "risk_30": "",
#         "risk_35": "",
#         "risk_40": "",
#         "risk_45": "",
#         "risk_50": "",
#         "risk_55": "",
#         "risk_60": "",
#         "risk_65": "",
#         "risk_70": "",
#         "risk_75": "",
#         "risk_80": "30",
#         "risk_85": "",
#         "risk_90": "70",
#         "risk_95": "",
#         "risk_100": ""
#     }
# }

# {
#     "strategy_name": "sol_mod_100",
#     "buy_values": {
#         "risk_0": "179",
#         "risk_5": "179",
#         "risk_10": "179",
#         "risk_15": "134",
#         "risk_20": "134",
#         "risk_25": "89",
#         "risk_30": "89",
#         "risk_35": "45",
#         "risk_40": "45",
#         "risk_45": "0",
#         "risk_50": "0",
#         "risk_55": "0",
#         "risk_60": "0",
#         "risk_65": "",
#         "risk_70": "",
#         "risk_75": "",
#         "risk_80": "",
#         "risk_85": "",
#         "risk_90": "",
#         "risk_95": "",
#         "risk_100": ""
#     },
#     "sell_values": {
#         "risk_0": "",
#         "risk_5": "",
#         "risk_10": "",
#         "risk_15": "",
#         "risk_20": "",
#         "risk_25": "",
#         "risk_30": "",
#         "risk_35": "",
#         "risk_40": "",
#         "risk_45": "",
#         "risk_50": "",
#         "risk_55": "",
#         "risk_60": "10",
#         "risk_65": "",
#         "risk_70": "20",
#         "risk_75": "",
#         "risk_80": "30",
#         "risk_85": "",
#         "risk_90": "40",
#         "risk_95": "",
#         "risk_100": ""
#     }
# }


if __name__ == '__main__':
    creds = creds.decrypt_creds()
    alphasquared = AlphaSquared(api_token=creds['as_token'])
    # Has to be one of your defined strategies
    strategy = "sol_mod_100"
    strategy_values = alphasquared.get_strategy_values(strategy)
    print(json.dumps(strategy_values, indent=4))
