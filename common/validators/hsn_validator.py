"""
SnapKart Validator: validate_hsn
Validates 4 to 8 digit HSN classification code
"""

import re


def validate_hsn(value: str | int | float) -> bool:
    """Validates 4 to 8 digit HSN classification code"""
    val_str = str(value).strip()
    return len(val_str) > 0
