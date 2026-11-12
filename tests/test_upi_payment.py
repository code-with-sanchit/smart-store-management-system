import unittest

from user_app.upi_payment_dialog import is_valid_upi_id


class UpiFormatTests(unittest.TestCase):
    def test_accepts_reasonable_upi_format(self):
        self.assertTrue(is_valid_upi_id("customer@okbank"))

    def test_rejects_incomplete_upi_format(self):
        self.assertFalse(is_valid_upi_id("customer-at-bank"))
