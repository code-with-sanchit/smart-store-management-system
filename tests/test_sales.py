import unittest
from decimal import Decimal

from common.sales import SaleError, calculate_sale_totals


class SaleTotalTests(unittest.TestCase):
    def test_totals_keep_two_decimal_precision(self):
        items = {1: {"name": "Milk", "price": "49.995", "qty": 2}}
        totals = calculate_sale_totals(items, delivery_fee="20", discount="5.50")
        self.assertEqual(totals.subtotal, Decimal("100.00"))
        self.assertEqual(totals.total, Decimal("114.50"))

    def test_discount_cannot_exceed_subtotal(self):
        items = {1: {"name": "Milk", "price": 50, "qty": 1}}
        with self.assertRaises(SaleError):
            calculate_sale_totals(items, discount=51)
