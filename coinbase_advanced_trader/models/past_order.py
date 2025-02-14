from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class PastOrder:
    strategy_name: str
    timestamp: datetime
    action: str
    order_id: str
    nearest_risk: Decimal
    value: Decimal
    balance: Decimal
    status: str
