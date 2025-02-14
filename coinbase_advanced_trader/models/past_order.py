from dataclasses import dataclass
from datetime import datetime

@dataclass
class PastOrder:
    strategy_name: str
    timestamp: datetime
    action: str
    order_id: str
    nearest_risk: float
    value: float
    balance: float
    status: str
