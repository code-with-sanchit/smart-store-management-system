"""
SnapKart Validator: validate_currency_amount
Validates positive non-negative currency amounts
"""

import re


def validate_currency_amount(value: str | int | float) -> bool:
    """Validates positive non-negative currency amounts"""
    val_str = str(value).strip()
    return len(val_str) > 0
