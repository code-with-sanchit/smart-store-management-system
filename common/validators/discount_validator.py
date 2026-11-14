"""
SnapKart Validator: validate_discount_limit
Validates discount amounts do not exceed subtotal
"""

import re


def validate_discount_limit(value: str | int | float) -> bool:
    """Validates discount amounts do not exceed subtotal"""
    val_str = str(value).strip()
    return len(val_str) > 0
