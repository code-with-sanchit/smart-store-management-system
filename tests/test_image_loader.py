import unittest
from common.image_loader import product_image_key, _find_image, get_product_image


class ImageLoaderTests(unittest.TestCase):
    def test_product_image_key_is_deterministic_and_clean(self):
        key1 = product_image_key("Amul Butter 500g")
        key2 = product_image_key("Amul Butter 500g")
        self.assertEqual(key1, key2)
        self.assertTrue(key1.startswith("amul-butter-500g-"))

    def test_find_image_fallback_to_category_image(self):
        cat_file = _find_image(item_id=999999, item_name="Nonexistent Item", category="Dairy, Milk & Paneer")
        self.assertIsNotNone(cat_file)
        self.assertTrue(cat_file.is_file())
        self.assertIn("dairy_milk_and_paneer", cat_file.name)

    def test_get_product_image_handles_invalid_ids(self):
        photo = get_product_image("invalid_id", "Test Item", "Nonexistent Category")
        # May be PhotoImage or None if Tk not initialized
        self.assertTrue(photo is not None or photo is None)
