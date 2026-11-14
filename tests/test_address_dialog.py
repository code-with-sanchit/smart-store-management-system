import unittest

from user_app.address_dialog import (
    DEFAULT_LOCALITIES,
    format_delivery_address,
    validate_address_fields
)


class AddressDialogLogicTests(unittest.TestCase):
    def test_default_localities_available(self):
        self.assertGreater(len(DEFAULT_LOCALITIES), 5)
        self.assertIn("Sanjay Place Commercial Hub", DEFAULT_LOCALITIES)
        self.assertIn("Civil Lines", DEFAULT_LOCALITIES)

    def test_format_delivery_address(self):
        addr = format_delivery_address("Flat 302, Palm Heights", "Civil Lines", "Agra", "282002")
        self.assertEqual(addr, "Flat 302, Palm Heights, Civil Lines, Agra - 282002")

    def test_format_delivery_address_minimal(self):
        addr = format_delivery_address("House 10", "Sanjay Place")
        self.assertEqual(addr, "House 10, Sanjay Place, Agra - 282002")

    def test_validate_address_success(self):
        valid, err = validate_address_fields("Flat 102", "Kamla Nagar", "282005", "+91 9876543210")
        self.assertTrue(valid)
        self.assertEqual(err, "")

    def test_validate_address_missing_house(self):
        valid, err = validate_address_fields("", "Kamla Nagar", "282005", "+91 9876543210")
        self.assertFalse(valid)
        self.assertIn("Flat / House number", err)

    def test_validate_address_missing_locality(self):
        valid, err = validate_address_fields("Flat 102", "", "282005", "+91 9876543210")
        self.assertFalse(valid)
        self.assertIn("delivery locality", err)

    def test_validate_address_invalid_pin(self):
        valid, err = validate_address_fields("Flat 102", "Kamla Nagar", "28", "+91 9876543210")
        self.assertFalse(valid)
        self.assertIn("PIN Code", err)

    def test_validate_address_invalid_phone(self):
        valid, err = validate_address_fields("Flat 102", "Kamla Nagar", "282005", "123")
        self.assertFalse(valid)
        self.assertIn("10-digit mobile number", err)
