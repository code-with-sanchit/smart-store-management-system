"""
SnapKart Domain Model: CustomerProfile
Customer account dataclass with contact details
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional


@dataclass
class CustomerProfile:
    """Customer account dataclass with contact details"""
    id: int | str
    name: str = ""
    created_at: Optional[datetime] = None
    active: bool = True
