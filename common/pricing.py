"""Pricing rules used by both checkout screens."""

FREE_DELIVERY_THRESHOLD = 499.0
STANDARD_DELIVERY_FEE = 20.0


def delivery_fee(subtotal: float) -> float:
    """Return the delivery charge for a non-empty customer order."""
    if subtotal <= 0:
        return 0.0
    return 0.0 if subtotal >= FREE_DELIVERY_THRESHOLD else STANDARD_DELIVERY_FEE
