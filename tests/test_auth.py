import unittest

from common.auth import hash_password, verify_password


class PasswordTests(unittest.TestCase):
    def test_hash_is_salted_and_verifiable(self):
        first = hash_password("safe-password")
        second = hash_password("safe-password")
        self.assertNotEqual(first, second)
        self.assertTrue(verify_password("safe-password", first))

    def test_rejects_wrong_password(self):
        self.assertFalse(verify_password("wrong", hash_password("correct")))
