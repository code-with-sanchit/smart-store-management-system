import unittest

from database.populate_inventory import generate_items


class CatalogTests(unittest.TestCase):
    def test_starter_catalog_is_unique_and_sellable(self):
        products = generate_items(600)
        self.assertEqual(len(products), 600)
        self.assertEqual(len({product[0] for product in products}), 600)
        self.assertTrue(all(price > 0 and stock > 0 for _, _, price, stock in products))
