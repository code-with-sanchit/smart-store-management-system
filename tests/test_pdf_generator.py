import tempfile
import unittest
from pathlib import Path

from common.pdf_generator import generate_pdf_receipt


class ReceiptTests(unittest.TestCase):
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
