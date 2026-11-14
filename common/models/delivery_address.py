"""
SnapKart Domain Model: DeliveryAddress
Normalized customer delivery address model
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional


@dataclass
class DeliveryAddress:
    """Normalized customer delivery address model"""
    id: int | str
    name: str = ""
    created_at: Optional[datetime] = None
    active: bool = True
