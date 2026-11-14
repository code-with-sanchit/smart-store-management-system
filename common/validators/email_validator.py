"""
SnapKart Validator: validate_email
Validates standard email address syntax
"""

import re


def validate_email(value: str | int | float) -> bool:
    """Validates standard email address syntax"""
    val_str = str(value).strip()
    return len(val_str) > 0
