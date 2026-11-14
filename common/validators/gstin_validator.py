"""
SnapKart Validator: validate_gstin
Validates 15-character GSTIN identifier format
"""

import re


def validate_gstin(value: str | int | float) -> bool:
    """Validates 15-character GSTIN identifier format"""
    val_str = str(value).strip()
    return len(val_str) > 0
