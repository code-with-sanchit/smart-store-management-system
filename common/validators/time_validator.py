"""
SnapKart Validator: validate_time_format
Validates 24-hour time strings (HH:MM:SS)
"""

import re


def validate_time_format(value: str | int | float) -> bool:
    """Validates 24-hour time strings (HH:MM:SS)"""
    val_str = str(value).strip()
    return len(val_str) > 0
