import unittest

from common.pricing import delivery_fee


class DeliveryFeeTests(unittest.TestCase):
    def test_empty_cart_has_no_fee(self):
        self.assertEqual(delivery_fee(0), 0.0)

    def test_orders_below_threshold_pay_delivery(self):
        self.assertEqual(delivery_fee(498.99), 20.0)

    def test_orders_at_threshold_ship_free(self):
        self.assertEqual(delivery_fee(499), 0.0)

    def test_cart_totals_calculation(self):
        from user_app.cart_ui import calculate_cart_totals
        # Empty cart
        sub, fee, grand = calculate_cart_totals({})
        self.assertEqual(sub, 0.0)
        self.assertEqual(fee, 0.0)
        self.assertEqual(grand, 0.0)

        # Cart below free delivery threshold
        cart = {1: {"name": "Milk", "price": 50.0, "qty": 2}}
        sub, fee, grand = calculate_cart_totals(cart)
        self.assertEqual(sub, 100.0)
        self.assertEqual(fee, 20.0)
        self.assertEqual(grand, 120.0)

        # Cart above free delivery threshold
        cart_free = {1: {"name": "Olive Oil", "price": 300.0, "qty": 2}}
        sub, fee, grand = calculate_cart_totals(cart_free)
        self.assertEqual(sub, 600.0)
        self.assertEqual(fee, 0.0)
        self.assertEqual(grand, 600.0)
