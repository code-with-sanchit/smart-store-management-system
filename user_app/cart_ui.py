"""
SnapKart User App - Cart Component Helper Module.
Provides auxiliary cart formatting, tax calculation, and receipt dialog helpers.
"""

from __future__ import annotations

from common.pricing import delivery_fee as calc_delivery_fee, calculate_tax


def calculate_cart_totals(
    cart_dict: dict,
    delivery_fee: float | None = None,
    discount: float = 0.0
) -> tuple[float, float, float, float]:
    """Computes subtotal, tax (5% GST), delivery fee, and grand total for active cart items."""
    subtotal = sum(float(item["price"]) * int(item["qty"]) for item in cart_dict.values())
    if subtotal <= 0:
        fee = 0.0
        tax = 0.0
    else:
        tax = calculate_tax(subtotal)
        if delivery_fee is not None:
            fee = float(delivery_fee)
        else:
            fee = calc_delivery_fee(subtotal)
    grand_total = round(subtotal + tax + fee - discount, 2)
    return subtotal, tax, fee, grand_total
