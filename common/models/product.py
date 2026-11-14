"""
SnapKart Domain Model: ProductRecord
Catalog product record with pricing and stock quantity
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional


@dataclass
class ProductRecord:
    """Catalog product record with pricing and stock quantity"""
    id: int | str
    name: str = ""
    created_at: Optional[datetime] = None
    active: bool = True
