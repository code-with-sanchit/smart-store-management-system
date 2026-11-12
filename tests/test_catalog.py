import unittest

from database.curated_catalog import CURATED_CATALOG, validate_catalog
from database.populate_inventory import generate_items


class CatalogTests(unittest.TestCase):
    def test_starter_catalog_is_unique_and_sellable(self):
        products = generate_items(600)
        self.assertEqual(len(products), len(CURATED_CATALOG))
        self.assertEqual(len({product[0] for product in products}), len(products))
        self.assertTrue(all(price > 0 and stock > 0 for _, _, price, stock in products))

    def test_catalog_is_not_randomized_between_runs(self):
        self.assertEqual(generate_items(12), generate_items(12))

    def test_curated_catalog_passes_its_quality_checks(self):
        self.assertEqual(validate_catalog(), [])
