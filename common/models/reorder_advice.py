"""
SnapKart Domain Model: ReorderAdvice
Inventory replenishment advisory model
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional


@dataclass
class ReorderAdvice:
    """Inventory replenishment advisory model"""
    id: int | str
    name: str = ""
    created_at: Optional[datetime] = None
    active: bool = True
