"""
SnapKart User App - Cart Component Helper Module.
Provides auxiliary cart formatting, tax calculation, and receipt dialog helpers.
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk


def calculate_cart_totals(cart_dict: dict, delivery_fee: float = 20.0) -> tuple[float, float, float]:
    """Computes subtotal, delivery fee, and grand total for active cart items."""
    subtotal = sum(float(item["price"]) * int(item["qty"]) for item in cart_dict.values())
    grand_total = subtotal + delivery_fee
    return subtotal, delivery_fee, grand_total
