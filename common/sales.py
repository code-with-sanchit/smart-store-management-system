"""Small, testable sale-recording service shared by both desktop checkout screens."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Mapping


MONEY_PLACES = Decimal("0.01")


class SaleError(ValueError):
    """Raised when a sale cannot safely be recorded."""


@dataclass(frozen=True)
class SaleTotals:
    subtotal: Decimal
    delivery_fee: Decimal
    discount: Decimal
    total: Decimal


def as_money(value: object) -> Decimal:
    """Convert a user or database value to a non-floating two-decimal amount."""
    return Decimal(str(value)).quantize(MONEY_PLACES, rounding=ROUND_HALF_UP)


def calculate_sale_totals(items: Mapping[object, Mapping[str, object]], delivery_fee=0, discount=0) -> SaleTotals:
    """Calculate an invoice total and reject invalid discounts before a database write."""
    subtotal = sum((as_money(row["price"]) * int(row["qty"]) for row in items.values()), Decimal("0.00"))
    fee = as_money(delivery_fee)
    reduction = as_money(discount)
    if subtotal <= 0:
        raise SaleError("Add at least one item before completing the sale.")
    if fee < 0 or reduction < 0:
        raise SaleError("Delivery fees and discounts cannot be negative.")
    if reduction > subtotal:
        raise SaleError("The discount cannot be greater than the product subtotal.")
    return SaleTotals(subtotal, fee, reduction, subtotal + fee - reduction)


def record_sale(connection, items, totals: SaleTotals, payment_method: str, customer_id=None, order_channel="store") -> int:
    """Atomically reserve stock and store an immutable invoice snapshot.

    The caller owns the connection. This function commits only after every stock
    reservation and line item succeeds, and rolls back on any failure.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO sales (sale_datetime, total_amount, payment_method, customer_id,
                               order_channel, delivery_fee, discount_amount)
            VALUES (NOW(), %s, %s, %s, %s, %s, %s)
            """,
            (totals.total, payment_method, customer_id, order_channel, totals.delivery_fee, totals.discount),
        )
        sale_id = cursor.lastrowid

        for item_id, item in items.items():
            quantity = int(item["qty"])
            if quantity < 1:
                raise SaleError(f"Quantity for {item['name']} must be at least one.")
            cursor.execute(
                "UPDATE inventory SET stock_quantity = stock_quantity - %s "
                "WHERE item_id = %s AND stock_quantity >= %s",
                (quantity, item_id, quantity),
            )
            if cursor.rowcount != 1:
                raise SaleError(f"{item['name']} is no longer available in the requested quantity.")

            unit_price = as_money(item["price"])
            line_total = (unit_price * quantity).quantize(MONEY_PLACES, rounding=ROUND_HALF_UP)
            cursor.execute(
                """
                INSERT INTO sale_items (sale_id, item_id, product_name, quantity, unit_price, subtotal)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (sale_id, item_id, str(item["name"])[:150], quantity, unit_price, line_total),
            )

        connection.commit()
        return sale_id
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
