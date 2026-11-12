import unittest
from datetime import time, timedelta
from common.store_status import check_store_status, is_time_in_window


class StoreStatusTests(unittest.TestCase):
    def test_check_store_status_returns_tuple(self):
        is_open, msg = check_store_status()
        self.assertIsInstance(is_open, bool)
        self.assertIsInstance(msg, str)
        self.assertGreater(len(msg), 0)

    def test_overnight_hours_cover_both_sides_of_midnight(self):
        self.assertTrue(is_time_in_window(time(23, 30), time(20), time(2)))
        self.assertTrue(is_time_in_window(time(1, 30), time(20), time(2)))
        self.assertFalse(is_time_in_window(time(10), time(20), time(2)))
