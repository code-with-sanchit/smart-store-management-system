"""Pricing and tax rules used by both checkout screens."""

FREE_DELIVERY_THRESHOLD = 499.0
STANDARD_DELIVERY_FEE = 20.0
GST_TAX_RATE = 0.05  # 5% GST (2.5% CGST + 2.5% SGST)


def delivery_fee(subtotal: float) -> float:
    """Return the delivery charge for a non-empty customer order."""
    if subtotal <= 0:
        return 0.0
    return 0.0 if subtotal >= FREE_DELIVERY_THRESHOLD else STANDARD_DELIVERY_FEE


def calculate_tax(subtotal: float) -> float:
    """Calculate 5% GST tax added to subtotal."""
    if subtotal <= 0:
        return 0.0
    return round(subtotal * GST_TAX_RATE, 2)


def calculate_tax_breakdown(subtotal: float) -> tuple[float, float, float]:
    """Return (total_tax, cgst, sgst) with 5% GST added."""
    if subtotal <= 0:
        return 0.0, 0.0, 0.0
    tax = round(subtotal * GST_TAX_RATE, 2)
    cgst = round(tax / 2, 2)
    sgst = round(tax - cgst, 2)
    return tax, cgst, sgst
