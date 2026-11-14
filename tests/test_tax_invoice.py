import os
import tempfile
import unittest
from pathlib import Path

from common.pdf_generator import generate_pdf_receipt
from common.sales import calculate_sale_totals


class TaxInvoiceTests(unittest.TestCase):
    def test_taxes_added_to_final_price(self):
        cart = {
            1: {"name": "Aashirvaad Atta 5kg", "price": 250.0, "qty": 2},
            2: {"name": "Amul Butter 500g", "price": 270.0, "qty": 1}
        }
        # Subtotal = 500 + 270 = 770.00
        # Delivery = 0.0 (over 499 threshold)
        # Tax (5% GST) = 38.50
        # Grand Total = 770 + 38.50 = 808.50
        totals = calculate_sale_totals(cart, delivery_fee=0, discount=0)
        self.assertEqual(float(totals.subtotal), 770.0)
        self.assertEqual(float(totals.tax), 38.50)
        self.assertEqual(float(totals.total), 808.50)

    def test_pdf_generation_with_explicit_taxes(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            cart = {
                1: {"name": "Tata Tea Gold 500g", "price": 315.0, "qty": 1}
            }
            totals = calculate_sale_totals(cart, delivery_fee=20.0, discount=10.0)
            # sub = 315, tax = 15.75, fee = 20, disc = 10 -> total = 340.75
            pdf_path = generate_pdf_receipt(
                sale_id=999,
                items_dict=cart,
                subtotal=totals.subtotal,
                delivery_fee=totals.delivery_fee,
                total_amount=totals.total,
                discount_amount=totals.discount,
                customer_name="Sanchit",
                customer_address="Sanjay Place, Agra",
                output_dir=tmp_dir
            )
            self.assertTrue(os.path.isfile(pdf_path))
            self.assertGreater(os.path.getsize(pdf_path), 5000)

