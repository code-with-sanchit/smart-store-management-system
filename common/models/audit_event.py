"""
SnapKart Domain Model: AuditEvent
System event log record for administrative tracking
"""

from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional


@dataclass
class AuditEvent:
    """System event log record for administrative tracking"""
    id: int | str
    name: str = ""
    created_at: Optional[datetime] = None
    active: bool = True
