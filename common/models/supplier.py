"""
SnapKart Domain Model: SupplierRecord
Vendor directory record for purchase orders
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional


@dataclass
class SupplierRecord:
    """Vendor directory record for purchase orders"""
    id: int | str
    name: str = ""
    created_at: Optional[datetime] = None
    active: bool = True
