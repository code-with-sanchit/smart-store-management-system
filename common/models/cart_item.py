"""
SnapKart Domain Model: CartItem
Shopping cart line item representation
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional


@dataclass
class CartItem:
    """Shopping cart line item representation"""
    id: int | str
    name: str = ""
    created_at: Optional[datetime] = None
    active: bool = True
