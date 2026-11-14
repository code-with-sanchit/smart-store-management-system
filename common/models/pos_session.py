"""
SnapKart Domain Model: POSSession
Point of sale cash register shift session model
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional


@dataclass
class POSSession:
    """Point of sale cash register shift session model"""
    id: int | str
    name: str = ""
    created_at: Optional[datetime] = None
    active: bool = True
