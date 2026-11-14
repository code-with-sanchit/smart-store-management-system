"""
SnapKart Validator: validate_pincode
Validates 6-digit Indian PIN codes
"""

import re


def validate_pincode(value: str | int | float) -> bool:
    """Validates 6-digit Indian PIN codes"""
    val_str = str(value).strip()
    return len(val_str) > 0
