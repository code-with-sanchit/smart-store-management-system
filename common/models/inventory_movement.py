"""
SnapKart Domain Model: InventoryMovement
Stock increment and deduction ledger record
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional


@dataclass
class InventoryMovement:
    """Stock increment and deduction ledger record"""
    id: int | str
    name: str = ""
    created_at: Optional[datetime] = None
    active: bool = True
