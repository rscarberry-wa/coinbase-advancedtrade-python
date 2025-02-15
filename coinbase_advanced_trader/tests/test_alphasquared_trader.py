import unittest
from unittest.mock import Mock
from decimal import Decimal
from coinbase_advanced_trader.alphasquared_trader import AlphaSquaredTrader
from coinbase_advanced_trader.models import Order, OrderSide, OrderType
from coinbase_advanced_trader.models.past_order import PastOrder
from datetime import datetime, timedelta


class TestAlphaSquaredTrader(unittest.TestCase):

    def setUp(self):
        self.mock_coinbase_client = Mock()
        self.mock_alphasquared_client = Mock()
        self.trader = AlphaSquaredTrader(self.mock_coinbase_client, self.mock_alphasquared_client)
        self.strategy_values_btc_agg_100 = {
            "strategy_name": "btc_agg_100",
            "buy_values": {
                "risk_0": "160",
                "risk_5": "160",
                "risk_10": "160",
                "risk_15": "140",
                "risk_20": "140",
                "risk_25": "120",
                "risk_30": "120",
                "risk_35": "100",
                "risk_40": "100",
                "risk_45": "80",
                "risk_50": "80",
                "risk_55": "60",
                "risk_60": "60",
                "risk_65": "40",
                "risk_70": "40",
                "risk_75": "0",
                "risk_80": "",
                "risk_85": "",
                "risk_90": "",
                "risk_95": "",
                "risk_100": ""
            },
            "sell_values": {
                "risk_0": "",
                "risk_5": "",
                "risk_10": "",
                "risk_15": "",
                "risk_20": "",
                "risk_25": "",
                "risk_30": "",
                "risk_35": "",
                "risk_40": "",
                "risk_45": "",
                "risk_50": "",
                "risk_55": "",
                "risk_60": "",
                "risk_65": "",
                "risk_70": "",
                "risk_75": "",
                "risk_80": "30",
                "risk_85": "",
                "risk_90": "70",
                "risk_95": "",
                "risk_100": ""
            }
        }
        self.strategy_values_eth_mod_100 = {
            "strategy_name": "eth_mod_100",
            "buy_values": {
                "risk_0": "179",
                "risk_5": "179",
                "risk_10": "179",
                "risk_15": "134",
                "risk_20": "134",
                "risk_25": "89",
                "risk_30": "89",
                "risk_35": "45",
                "risk_40": "45",
                "risk_45": "0",
                "risk_50": "0",
                "risk_55": "0",
                "risk_60": "0",
                "risk_65": "",
                "risk_70": "",
                "risk_75": "",
                "risk_80": "",
                "risk_85": "",
                "risk_90": "",
                "risk_95": "",
                "risk_100": ""
            },
            "sell_values": {
                "risk_0": "",
                "risk_5": "",
                "risk_10": "",
                "risk_15": "",
                "risk_20": "",
                "risk_25": "",
                "risk_30": "",
                "risk_35": "",
                "risk_40": "",
                "risk_45": "",
                "risk_50": "",
                "risk_55": "",
                "risk_60": "10",
                "risk_65": "",
                "risk_70": "20",
                "risk_75": "",
                "risk_80": "30",
                "risk_85": "",
                "risk_90": "40",
                "risk_95": "",
                "risk_100": ""
            }
        }
        self.strategy_values_sol_mod_100 = {
            "strategy_name": "sol_mod_100",
            "buy_values": {
                "risk_0": "179",
                "risk_5": "179",
                "risk_10": "179",
                "risk_15": "134",
                "risk_20": "134",
                "risk_25": "89",
                "risk_30": "89",
                "risk_35": "45",
                "risk_40": "45",
                "risk_45": "0",
                "risk_50": "0",
                "risk_55": "0",
                "risk_60": "0",
                "risk_65": "",
                "risk_70": "",
                "risk_75": "",
                "risk_80": "",
                "risk_85": "",
                "risk_90": "",
                "risk_95": "",
                "risk_100": ""
            },
            "sell_values": {
                "risk_0": "",
                "risk_5": "",
                "risk_10": "",
                "risk_15": "",
                "risk_20": "",
                "risk_25": "",
                "risk_30": "",
                "risk_35": "",
                "risk_40": "",
                "risk_45": "",
                "risk_50": "",
                "risk_55": "",
                "risk_60": "10",
                "risk_65": "",
                "risk_70": "20",
                "risk_75": "",
                "risk_80": "30",
                "risk_85": "",
                "risk_90": "40",
                "risk_95": "",
                "risk_100": ""
            }
        }

    def test_get_strategy_recommendation_buy_sol1(self):
        self.mock_alphasquared_client.get_strategy_values.return_value = self.strategy_values_sol_mod_100

        recommendation = self.trader.get_strategy_recommendation('SOL-USD', 'sol_mod_100', 41.0, None)

        self.mock_alphasquared_client.get_strategy_values.assert_called_once_with('sol_mod_100')
        assert recommendation.action == 'buy'
        assert recommendation.value == Decimal(45.0)
        assert recommendation.nearest_risk == Decimal(35.0)

    def test_get_strategy_recommendation_buy_sol1(self):
        self.mock_alphasquared_client.get_strategy_values.return_value = self.strategy_values_sol_mod_100

        recommendation = self.trader.get_strategy_recommendation('SOL-USD', 'sol_mod_100', 45.0, None)

        self.mock_alphasquared_client.get_strategy_values.assert_called_once_with('sol_mod_100')
        assert recommendation is None

    def test_get_strategy_recommendation_buy_bth1(self):
        self.mock_alphasquared_client.get_strategy_values.return_value = self.strategy_values_btc_agg_100

        recommendation = self.trader.get_strategy_recommendation('BTC-USDC', 'btc_agg_100', 55.0, None)

        self.mock_alphasquared_client.get_strategy_values.assert_called_once_with('btc_agg_100')
        assert recommendation.action == 'buy'
        assert recommendation.value == Decimal(60.0)
        assert recommendation.nearest_risk == 55.0

    # Test with same risk and strategy values, but within 7 days
    def test_get_strategy_recommendation_buy_bth2(self):
        self.mock_alphasquared_client.get_strategy_values.return_value = self.strategy_values_btc_agg_100

        recommendation = self.trader.get_strategy_recommendation('BTC-USDC', 'btc_agg_100', 55.0,
                                                                 PastOrder(strategy_name='btc_agg_100',
                                                                           timestamp=datetime.now() - timedelta(days=3),
                                                                           action='buy',
                                                                           order_id="32343",
                                                                           nearest_risk=55.0,
                                                                           value=60.0,
                                                                           balance=0.0,
                                                                           status="success"))

        self.mock_alphasquared_client.get_strategy_values.assert_called_once_with('btc_agg_100')
        assert recommendation is None

    # Test with a risk that matches a higher nearest risk, but with the same buy amount
    def test_get_strategy_recommendation_buy_bth3(self):
        self.mock_alphasquared_client.get_strategy_values.return_value = self.strategy_values_btc_agg_100

        recommendation = self.trader.get_strategy_recommendation('BTC-USDC', 'btc_agg_100', 61.0,
                                                                 PastOrder(strategy_name='btc_agg_100',
                                                                           timestamp=datetime.now() - timedelta(days=3),
                                                                           action='buy',
                                                                           order_id="32343",
                                                                           nearest_risk=55.0,
                                                                           value=60.0,
                                                                           balance=0.0,
                                                                           status="success"))

        self.mock_alphasquared_client.get_strategy_values.assert_called_once_with('btc_agg_100')
        assert recommendation is None

    # Test with a risk that matches the same risk, but 7 days have passed
    def test_get_strategy_recommendation_buy_bth4(self):
        self.mock_alphasquared_client.get_strategy_values.return_value = self.strategy_values_btc_agg_100

        recommendation = self.trader.get_strategy_recommendation('BTC-USDC', 'btc_agg_100', 55.0,
                                                                 PastOrder(strategy_name='btc_agg_100',
                                                                           timestamp=datetime.now() - timedelta(days=7),
                                                                           action='buy',
                                                                           order_id="32343",
                                                                           nearest_risk=55.0,
                                                                           value=60.0,
                                                                           balance=0.0,
                                                                           status="success"))

        self.mock_alphasquared_client.get_strategy_values.assert_called_once_with('btc_agg_100')
        assert recommendation.action == 'buy'
        assert recommendation.value == Decimal(60.0)
        assert recommendation.nearest_risk == 55.0

    # Test with a higher risk that matches a higher band, and less than 7 days have passed
    def test_get_strategy_recommendation_buy_bth5(self):
        self.mock_alphasquared_client.get_strategy_values.return_value = self.strategy_values_btc_agg_100

        recommendation = self.trader.get_strategy_recommendation('BTC-USDC', 'btc_agg_100', 65.0,
                                                                 PastOrder(strategy_name='btc_agg_100',
                                                                           timestamp=datetime.now() - timedelta(days=3),
                                                                           action='buy',
                                                                           order_id="32343",
                                                                           nearest_risk=55.0,
                                                                           value=60.0,
                                                                           balance=0.0,
                                                                           status="success"))

        self.mock_alphasquared_client.get_strategy_values.assert_called_once_with('btc_agg_100')
        assert recommendation is None

    # Test with a lower risk that matches a lower band, and less than 7 days have passed
    def test_get_strategy_recommendation_buy_bth6(self):
        self.mock_alphasquared_client.get_strategy_values.return_value = self.strategy_values_btc_agg_100

        recommendation = self.trader.get_strategy_recommendation('BTC-USDC', 'btc_agg_100', 45.0,
                                                                 PastOrder(strategy_name='btc_agg_100',
                                                                           timestamp=datetime.now() - timedelta(days=3),
                                                                           action='buy',
                                                                           order_id="32343",
                                                                           nearest_risk=55.0,
                                                                           value=60.0,
                                                                           balance=0.0,
                                                                           status="success"))

        self.mock_alphasquared_client.get_strategy_values.assert_called_once_with('btc_agg_100')
        assert recommendation.action == 'buy'
        assert recommendation.value == Decimal(80.0)
        assert recommendation.nearest_risk == 45.0

    def test_get_strategy_recommendation_sell_bth1(self):
        self.mock_alphasquared_client.get_strategy_values.return_value = self.strategy_values_btc_agg_100
        self.mock_coinbase_client.get_crypto_balance.return_value = 1.0

        recommendation = self.trader.get_strategy_recommendation('BTC', 'btc_agg_100', 82.0, None)

        self.mock_alphasquared_client.get_strategy_values.assert_called_once_with('btc_agg_100')
        self.mock_coinbase_client.get_crypto_balance.assert_called_once_with('BTC')

        assert recommendation.action == 'sell'
        assert recommendation.value == Decimal('0.3')
        assert recommendation.nearest_risk == 80.0
        assert recommendation.balance == 1.0

    def test_get_strategy_recommendation_sell_bth2(self):
        self.mock_alphasquared_client.get_strategy_values.return_value = self.strategy_values_btc_agg_100
        self.mock_coinbase_client.get_crypto_balance.return_value = Decimal('1.0')

        recommendation = self.trader.get_strategy_recommendation('BTC', 'btc_agg_100', 87.0,
                                                                 PastOrder(strategy_name='btc_agg_100',
                                                                           timestamp=datetime.now() - timedelta(days=2),
                                                                           action='sell',
                                                                           order_id="32343",
                                                                           nearest_risk=80.0,
                                                                           value=0.3,
                                                                           balance=1.0,
                                                                           status="success"))

        self.mock_alphasquared_client.get_strategy_values.assert_called_once_with('btc_agg_100')

        assert recommendation is None

    def test_get_strategy_recommendation_sell_bth3(self):
        self.mock_alphasquared_client.get_strategy_values.return_value = self.strategy_values_btc_agg_100

        recommendation = self.trader.get_strategy_recommendation('BTC', 'btc_agg_100', 91.0,
                                                                 PastOrder(strategy_name='btc_agg_100',
                                                                           timestamp=datetime.now() - timedelta(days=2),
                                                                           action='sell',
                                                                           order_id="32343",
                                                                           nearest_risk=80.0,
                                                                           value=0.3,
                                                                           balance=1.0,
                                                                           status="success"))

        self.mock_alphasquared_client.get_strategy_values.assert_called_once_with('btc_agg_100')

        assert recommendation.action == 'sell'
        assert recommendation.value == Decimal('0.7')
        assert recommendation.nearest_risk == 90.0
        assert recommendation.balance == 1.0

    def test_execute_strategy_buy(self):
        self.mock_alphasquared_client.get_current_risk.return_value = 30
        self.mock_alphasquared_client.get_strategy_values.return_value = self.strategy_values_eth_mod_100

        mock_order = Order(
            id='123',
            product_id='ETH-USD',
            side=OrderSide.BUY,
            type=OrderType.LIMIT,
            size=Decimal('0.001'),
            price=Decimal('50000')
        )

        self.mock_coinbase_client.fiat_limit_buy.return_value = mock_order

        past_order = self.trader.execute_strategy('ETH-USD', 'eth_mod_100')

        self.mock_alphasquared_client.get_current_risk.assert_called_once_with('ETH')
        self.mock_alphasquared_client.get_strategy_values.assert_called_once_with('eth_mod_100')
        self.mock_coinbase_client.fiat_limit_buy.assert_called_once_with('ETH-USD', '89', price_multiplier=0.995)

        assert past_order is not None
        assert past_order.strategy_name == 'eth_mod_100'
        assert past_order.action == 'buy'
        assert past_order.order_id == '123'
        assert past_order.nearest_risk == 25
        assert past_order.value == 89.0
        assert past_order.balance == 0.0
        assert past_order.status == 'pending'

    def test_execute_strategy_sell(self):
        self.mock_alphasquared_client.get_current_risk.return_value = 61.
        self.mock_alphasquared_client.get_strategy_values.return_value = self.strategy_values_eth_mod_100

        self.mock_coinbase_client.get_crypto_balance.return_value = '1.0'
        self.mock_coinbase_client.get_product.return_value = {
            'base_increment': '0.00000001',
            'quote_increment': '0.01',
            'price': '50000'
        }

        mock_order = Order(
            id='456',
            product_id='ETH-USD',
            side=OrderSide.SELL,
            type=OrderType.LIMIT,
            size=Decimal('0.5'),
            price=Decimal('50250')
        )
        self.mock_coinbase_client.limit_order_gtc_sell.return_value = mock_order

        past_order = self.trader.execute_strategy('ETH-USD', 'eth_mod_100')

        self.mock_alphasquared_client.get_current_risk.assert_called_once_with('ETH')
        self.mock_alphasquared_client.get_strategy_values.assert_called_once_with('eth_mod_100')
        assert self.mock_coinbase_client.get_crypto_balance.call_count == 2
        self.mock_coinbase_client.get_product.assert_called_once_with('ETH-USD')
        self.mock_coinbase_client.limit_order_gtc_sell.assert_called_once()

        assert past_order is not None
        assert past_order.strategy_name == 'eth_mod_100'
        assert past_order.action == 'sell'
        assert past_order.order_id == '456'
        assert past_order.nearest_risk == Decimal('60.0')
        assert past_order.value == Decimal('0.1')
        assert past_order.balance == Decimal('1.0')
        assert past_order.status == 'pending'

    def test_execute_multiple_buys_and_sells_no_delays_between(self):
        risks = [19., 22.0, 25., 20.0, 13., 22.0, 28., 31., 44., 42., 51., 63., 70., 72., 80., 95.]
        expected_actions = {
            0: ('buy', Decimal('134'), 15.),
            4: ('buy', Decimal('179'), 0.),
            11: ('sell', Decimal('0.1'), 60.),
            12: ('sell', Decimal('0.2'), 70.),
            14: ('sell', Decimal('0.3'), 80.),
            15: ('sell', Decimal('0.4'), 90.)
        }
        self.mock_alphasquared_client.get_current_risk.side_effect = risks
        self.mock_alphasquared_client.get_strategy_values.return_value = self.strategy_values_eth_mod_100
        self.mock_coinbase_client.get_crypto_balance.return_value = '1.0'
        past_order = None
        for index, risk in enumerate(risks):
            recommendation = self.trader.get_strategy_recommendation('ETH-USD', 'eth_mod_100', risk, past_order)
            #print(f"Index: {index}, risk: {risk}, recommendation: {recommendation}")
            if index in expected_actions:
                assert recommendation is not None
                expected_action, expected_value, expected_nearest_risk = expected_actions[index]
                assert recommendation.action == expected_action
                assert recommendation.value == expected_value
                assert recommendation.nearest_risk == expected_nearest_risk
            if recommendation:
                past_order = PastOrder(
                    strategy_name='eth_mod_100',
                    timestamp=datetime.now(),
                    action=recommendation.action,
                    order_id="32343",
                    nearest_risk=recommendation.nearest_risk,
                    value=float(recommendation.value),
                    balance=float(recommendation.balance),
                    status="success"
                )
            else:
                assert recommendation is None

    def test_execute_multiple_buys_and_sells_high_delays_between(self):
        risks = [19., 22.0, 25., 20.0, 13., 22.0, 28., 31., 44., 42., 51., 63., 70., 72., 80., 95.]
        expected_actions = {
            0: ('buy', Decimal('134'), 15.),
            1: ('buy', Decimal('134'), 15.),
            2: ('buy', Decimal('89'), 25.),
            3: ('buy', Decimal('134'), 15.),
            4: ('buy', Decimal('179'), 0.),
            5: ('buy', Decimal('134'), 15.),
            6: ('buy', Decimal('89'), 25.),
            7: ('buy', Decimal('89'), 25.),
            8: ('buy', Decimal('45'), 35.),
            9: ('buy', Decimal('45'), 35.),
            11: ('sell', Decimal('0.1'), 60.),
            12: ('sell', Decimal('0.2'), 70.),
            14: ('sell', Decimal('0.3'), 80.),
            15: ('sell', Decimal('0.4'), 90.)
        }
        self.mock_alphasquared_client.get_strategy_values.return_value = self.strategy_values_eth_mod_100
        self.mock_coinbase_client.get_crypto_balance.return_value = '1.0'
        past_order = None
        for index, risk in enumerate(risks):
            recommendation = self.trader.get_strategy_recommendation('ETH-USD', 'eth_mod_100', risk, past_order)
            #print(f"Index: {index}, risk: {risk}, recommendation: {recommendation}")
            if index in expected_actions:
                assert recommendation is not None
                expected_action, expected_value, expected_nearest_risk = expected_actions[index]
                assert recommendation.action == expected_action
                assert recommendation.value == expected_value
                assert recommendation.nearest_risk == expected_nearest_risk
            if recommendation:
                past_order = PastOrder(
                    strategy_name='eth_mod_100',
                    timestamp=datetime.now() - timedelta(days=7),
                    action=recommendation.action,
                    order_id="32343",
                    nearest_risk=recommendation.nearest_risk,
                    value=float(recommendation.value),
                    balance=float(recommendation.balance),
                    status="success"
                )
            else:
                assert recommendation is None


if __name__ == '__main__':
    unittest.main()
