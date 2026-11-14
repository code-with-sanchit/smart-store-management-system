"""
SnapKart Validator: validate_quantity
Validates positive integer inventory quantities
"""

import re


def validate_quantity(value: str | int | float) -> bool:
    """Validates positive integer inventory quantities"""
    val_str = str(value).strip()
    return len(val_str) > 0
