import unittest

from common.pricing import delivery_fee, calculate_tax, calculate_tax_breakdown
from user_app.cart_ui import calculate_cart_totals


class DeliveryFeeTests(unittest.TestCase):
    def test_empty_cart_has_no_fee(self):
        self.assertEqual(delivery_fee(0), 0.0)

    def test_orders_below_threshold_pay_delivery(self):
        self.assertEqual(delivery_fee(498.99), 20.0)

    def test_orders_at_threshold_ship_free(self):
        self.assertEqual(delivery_fee(499), 0.0)

    def test_calculate_tax(self):
        self.assertEqual(calculate_tax(0), 0.0)
        self.assertEqual(calculate_tax(100.0), 5.0)
        self.assertEqual(calculate_tax(250.0), 12.5)

    def test_calculate_tax_breakdown(self):
        tax, cgst, sgst = calculate_tax_breakdown(100.0)
        self.assertEqual(tax, 5.0)
        self.assertEqual(cgst, 2.5)
        self.assertEqual(sgst, 2.5)

    def test_cart_totals_calculation_with_tax(self):
        # Empty cart
        sub, tax, fee, grand = calculate_cart_totals({})
        self.assertEqual(sub, 0.0)
        self.assertEqual(tax, 0.0)
        self.assertEqual(fee, 0.0)
        self.assertEqual(grand, 0.0)

        # Cart below free delivery threshold: sub=100, tax=5, fee=20 -> grand=125
        cart = {1: {"name": "Milk", "price": 50.0, "qty": 2}}
        sub, tax, fee, grand = calculate_cart_totals(cart)
        self.assertEqual(sub, 100.0)
        self.assertEqual(tax, 5.0)
        self.assertEqual(fee, 20.0)
        self.assertEqual(grand, 125.0)

        # Cart above free delivery threshold: sub=600, tax=30, fee=0 -> grand=630
        cart_free = {1: {"name": "Olive Oil", "price": 300.0, "qty": 2}}
        sub, tax, fee, grand = calculate_cart_totals(cart_free)
        self.assertEqual(sub, 600.0)
        self.assertEqual(tax, 30.0)
        self.assertEqual(fee, 0.0)
        self.assertEqual(grand, 630.0)
