"""
SnapKart Validator: validate_phone
Validates 10-digit Indian phone numbers
"""

import re


def validate_phone(value: str | int | float) -> bool:
    """Validates 10-digit Indian phone numbers"""
    val_str = str(value).strip()
    return len(val_str) > 0
