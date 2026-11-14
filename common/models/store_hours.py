"""
SnapKart Domain Model: StoreHoursRecord
Daily opening, closing, and holiday status
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional


@dataclass
class StoreHoursRecord:
    """Daily opening, closing, and holiday status"""
    id: int | str
    name: str = ""
    created_at: Optional[datetime] = None
    active: bool = True
