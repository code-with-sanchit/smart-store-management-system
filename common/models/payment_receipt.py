"""
SnapKart Domain Model: PaymentReceipt
Receipt verification record with UPI reference
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional


@dataclass
class PaymentReceipt:
    """Receipt verification record with UPI reference"""
    id: int | str
    name: str = ""
    created_at: Optional[datetime] = None
    active: bool = True
