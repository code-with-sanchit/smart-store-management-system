"""
SnapKart Domain Model: DiscountRule
Promotional discount rules and caps
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional


@dataclass
class DiscountRule:
    """Promotional discount rules and caps"""
    id: int | str
    name: str = ""
    created_at: Optional[datetime] = None
    active: bool = True
