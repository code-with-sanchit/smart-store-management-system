import unittest
from datetime import time, timedelta
from common.store_status import check_store_status


class StoreStatusTests(unittest.TestCase):
    def test_check_store_status_returns_tuple(self):
        is_open, msg = check_store_status()
        self.assertIsInstance(is_open, bool)
        self.assertIsInstance(msg, str)
        self.assertGreater(len(msg), 0)
