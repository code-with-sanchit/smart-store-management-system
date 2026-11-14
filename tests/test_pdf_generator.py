import tempfile
import unittest
from pathlib import Path

from datetime import datetime

from common.pdf_generator import generate_pdf_receipt, invoice_number


class ReceiptTests(unittest.TestCase):
    def test_invoice_number_uses_the_issue_year(self):
        self.assertEqual(invoice_number(42, datetime(2027, 1, 1)), "SK-2027-000042")

    def test_receipt_is_written_with_discount_line(self):
        with tempfile.TemporaryDirectory() as folder:
            result = generate_pdf_receipt(
                sale_id=42,
                items_dict={1: {"name": "Test Product", "price": 100, "qty": 1}},
                subtotal=100,
                delivery_fee=20,
                discount_amount=10,
                total_amount=110,
                output_dir=folder,
            )
            pdf_path = Path(result)
            self.assertTrue(pdf_path.is_file())
            self.assertGreater(pdf_path.stat().st_size, 1000)
