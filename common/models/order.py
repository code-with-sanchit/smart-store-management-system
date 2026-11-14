"""
SnapKart Domain Model: OrderSnapshot
Immutable order snapshot containing line items and totals
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional


@dataclass
class OrderSnapshot:
    """Immutable order snapshot containing line items and totals"""
    id: int | str
    name: str = ""
    created_at: Optional[datetime] = None
    active: bool = True
