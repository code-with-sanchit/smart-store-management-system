"""
SnapKart User App - Cart Component Helper Module.
Provides auxiliary cart formatting, tax calculation, and receipt dialog helpers.
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk


from common.pricing import delivery_fee as calc_delivery_fee


def calculate_cart_totals(cart_dict: dict, delivery_fee: float | None = None) -> tuple[float, float, float]:
    """Computes subtotal, delivery fee, and grand total for active cart items."""
    subtotal = sum(float(item["price"]) * int(item["qty"]) for item in cart_dict.values())
    if subtotal <= 0:
        fee = 0.0
    elif delivery_fee is not None:
        fee = float(delivery_fee)
    else:
        fee = calc_delivery_fee(subtotal)
    grand_total = subtotal + fee
    return subtotal, fee, grand_total
