"""
SnapKart Domain Model: TaxBreakdown
GST tax computation with CGST and SGST allocation
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional


@dataclass
class TaxBreakdown:
    """GST tax computation with CGST and SGST allocation"""
    id: int | str
    name: str = ""
    created_at: Optional[datetime] = None
    active: bool = True
