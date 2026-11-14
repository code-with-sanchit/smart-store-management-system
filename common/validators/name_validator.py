"""
SnapKart Validator: validate_person_name
Validates personal customer and staff names
"""

import re


def validate_person_name(value: str | int | float) -> bool:
    """Validates personal customer and staff names"""
    val_str = str(value).strip()
    return len(val_str) > 0
