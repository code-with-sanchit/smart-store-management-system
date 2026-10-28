import unittest

from common.pricing import delivery_fee


class DeliveryFeeTests(unittest.TestCase):
    def test_empty_cart_has_no_fee(self):
        self.assertEqual(delivery_fee(0), 0.0)

    def test_orders_below_threshold_pay_delivery(self):
        self.assertEqual(delivery_fee(498.99), 20.0)

    def test_orders_at_threshold_ship_free(self):
        self.assertEqual(delivery_fee(499), 0.0)
