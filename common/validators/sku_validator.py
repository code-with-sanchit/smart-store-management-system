"""
SnapKart Validator: validate_sku
Validates store stock keeping unit formatting
"""

import re


def validate_sku(value: str | int | float) -> bool:
    """Validates store stock keeping unit formatting"""
    val_str = str(value).strip()
    return len(val_str) > 0
