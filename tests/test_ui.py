import unittest

from common.ui import Debouncer


class FakeWidget:
    def __init__(self):
        self.cancelled = []

    def after(self, delay, callback):
        return f"job-{delay}"

    def after_cancel(self, job):
        self.cancelled.append(job)


class DebouncerTests(unittest.TestCase):
    def test_cancel_removes_pending_callback(self):
        widget = FakeWidget()
        debouncer = Debouncer(widget)
        debouncer.call(lambda: None)
        debouncer.cancel()
        self.assertEqual(widget.cancelled, ["job-250"])
        self.assertIsNone(debouncer._job)
