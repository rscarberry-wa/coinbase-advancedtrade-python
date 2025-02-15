from decimal import Decimal, ROUND_DOWN
import logging
import math
from .enhanced_rest_client import EnhancedRESTClient
from alphasquared import AlphaSquared
from coinbase_advanced_trader.models import Order, PastOrder
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .models.past_order import PastOrder

logger = logging.getLogger(__name__)

@dataclass
class StrategyRecommendation:
    action: str
    value: Decimal
    nearest_risk: Decimal
    balance: Decimal

class AlphaSquaredTrader:
    def __init__(self, coinbase_client: EnhancedRESTClient, alphasquared_client: AlphaSquared):
        self.coinbase_client = coinbase_client
        self.alphasquared_client = alphasquared_client

    def execute_strategy(self, product_id: str, strategy_name: str,
                         past_order: Optional[PastOrder] = None, dry_run: bool = False):
        try:
            asset, base_currency = product_id.split('-')
            
            current_risk = self.alphasquared_client.get_current_risk(asset)
            logger.info(f"Current {asset} Risk: {current_risk}")

            recommendation = self.get_strategy_recommendation(asset, strategy_name, current_risk, past_order)
            if recommendation is None or recommendation.value <= 0:
                logger.info("No action taken based on current risk and strategy.")
                return None

            logger.info(f"Strategy suggests: Action = {recommendation.action.upper()}, Value = {recommendation.value}")
            if dry_run:
                logger.info("No action taken due to dry run.")
                return None

            if recommendation.action.lower() == 'buy':
                order = self._execute_buy(product_id, recommendation.value)
                if order is not None:
                    return self._to_past_order(strategy_name, order, recommendation)
            elif recommendation.action.lower() == 'sell':
                order = self._execute_sell(product_id, asset, base_currency, recommendation.value)
                if order is not None:
                    return self._to_past_order(strategy_name, order, recommendation)
            else:
                logger.info(f"Unknown action: {recommendation.action}. No trade executed.")
                return None
        except Exception as e:
            logger.error(f"Error in execute_strategy: {str(e)}")
            logger.exception("Full traceback:")
            return None

    def _execute_buy(self, product_id: str, value: Decimal) -> Optional[Order]:
        try:
            order = self.coinbase_client.fiat_limit_buy(product_id, str(value), price_multiplier=0.995)
            if isinstance(order, Order):
                logger.info(f"Buy limit order placed: ID={order.id}, Size={order.size}, Price={order.price}")
                return order
            else:
                logger.warning(f"Unexpected order response type: {type(order)}")
                return None
        except Exception as e:
            logger.error(f"Error placing buy order: {str(e)}")
            logger.exception("Full traceback:")
            return None

    def _execute_sell(self, product_id, asset, base_currency, value):
        balance = Decimal(self.coinbase_client.get_crypto_balance(asset))
        logger.info(f"Current {asset} balance: {balance}")
        
        product_details = self.coinbase_client.get_product(product_id)
        base_increment = Decimal(product_details['base_increment'])
        quote_increment = Decimal(product_details['quote_increment'])
        current_price = Decimal(product_details['price'])
        logger.info(f"Current {asset} price: {current_price} {base_currency}")

        sell_amount = min(value, balance).quantize(base_increment, rounding=ROUND_DOWN)
        logger.info(f"Sell amount: {sell_amount} {asset}")

        if sell_amount > base_increment:
            limit_price = (current_price * Decimal('1.005')).quantize(quote_increment, rounding=ROUND_DOWN)
            
            order = self.coinbase_client.limit_order_gtc_sell(
                client_order_id=self.coinbase_client._order_service._generate_client_order_id(),
                product_id=product_id,
                base_size=str(sell_amount),
                limit_price=str(limit_price)
            )
            if isinstance(order, Order):
                logger.info(f"Sell limit order placed for {sell_amount} {asset} at {limit_price} {base_currency}: {order}")
                return order
            else:
                logger.warning(f"Unexpected order response type: {type(order)}")
                return None
        else:
            logger.info(f"Sell amount {sell_amount} {asset} is too small. Minimum allowed is {base_increment}. No order placed.")
            return None

    def get_strategy_recommendation(self, asset: str, strategy_name: str, risk: float, past_order: Optional[PastOrder]) -> Optional[StrategyRecommendation]:
        """
        Get the strategy recommendation for a specific strategy and risk level

        :param strategy_name: The name of the strategy
        :param risk: The risk level (0-100, can be float)
        :param past_order: The past order object, if any, to consider for the recommendation
        :return: A optional StrategyRecommendation object, None, for no recommendation or an error
        """
        strategy_values = self.alphasquared_client.get_strategy_values(strategy_name)
        buy_values = strategy_values.get("buy_values", {})
        sell_values = strategy_values.get("sell_values", {})

        risk_levels = sorted(set([int(k.split('_')[1]) for k in buy_values.keys() if not self._empty_or_zero(buy_values[k])] +
                                 [int(k.split('_')[1]) for k in sell_values.keys() if not self._empty_or_zero(sell_values[k])]))

        nearest_risk = max([r for r in risk_levels if r <= risk], default=min(risk_levels))

        buy_value = float(buy_values.get(f"risk_{nearest_risk}", "0") or 0)
        sell_value = float(sell_values.get(f"risk_{nearest_risk}", "0") or 0)

        if buy_value > sell_value:
            if past_order is not None and past_order.action == "buy":
                if ((datetime.now() - past_order.timestamp).days >= 7 or
                        (past_order.nearest_risk - nearest_risk >= 5 and not math.isclose(buy_value, past_order.value, abs_tol=1e-3))):
                    return StrategyRecommendation("buy", Decimal(buy_value), Decimal(nearest_risk), Decimal(0))
            else:
                return StrategyRecommendation("buy", Decimal(buy_value), Decimal(nearest_risk), Decimal(0))
        elif sell_value > buy_value:
            if past_order is not None and past_order.action == "sell":
                if nearest_risk - past_order.nearest_risk >= 5:
                    amount_to_sell = (Decimal(past_order.balance) * Decimal(sell_value) / Decimal('100'))
                    return StrategyRecommendation("sell", amount_to_sell, Decimal(nearest_risk), Decimal(past_order.balance))
                else:
                    return None
            else:
                balance = Decimal(self.coinbase_client.get_crypto_balance(asset))
                amount_to_sell = (balance * Decimal(sell_value) / Decimal('100'))
                return StrategyRecommendation("sell", amount_to_sell, Decimal(nearest_risk), balance)
        else:
            return None

    def _to_past_order(self, strategy_name: str, order: Order, recommendation: StrategyRecommendation) -> PastOrder:
        return PastOrder(strategy_name=strategy_name,
                         timestamp=datetime.now(),
                         action=recommendation.action,
                         order_id=order.id,
                         nearest_risk=recommendation.nearest_risk,
                         value=recommendation.value,
                         balance=recommendation.balance,
                         status=order.status)

    def _empty_or_zero(self, s: str) -> bool:
        return not s or s == "0"
