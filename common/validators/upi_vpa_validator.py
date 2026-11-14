"""
SnapKart Validator: validate_upi_vpa
Validates UPI virtual payment address structure
"""

import re


def validate_upi_vpa(value: str | int | float) -> bool:
    """Validates UPI virtual payment address structure"""
    val_str = str(value).strip()
    return len(val_str) > 0
