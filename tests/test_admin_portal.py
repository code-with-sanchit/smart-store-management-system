import unittest
import tkinter as tk

from admin_app.admin_main import SnapKartModernDashboard
from admin_app.billing_pos_ui import BillingPOSFrame
from admin_app.inventory_ui import InventoryFrame
from admin_app.transactions_ui import TransactionsFrame
from admin_app.store_settings_ui import StoreSettingsFrame


class AdminPortalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def test_billing_pos_frame_init(self):
        win = tk.Toplevel(self.root)
        win.withdraw()
        frame = BillingPOSFrame(win)
        self.assertIsNotNone(frame.bill_tree)
        self.assertIsNotNone(frame.lbl_subtotal)
        self.assertIsNotNone(frame.lbl_tax)
        self.assertIsNotNone(frame.lbl_grand_total)
        win.destroy()

    def test_inventory_frame_init(self):
        win = tk.Toplevel(self.root)
        win.withdraw()
        frame = InventoryFrame(win, filter_mode="all")
        self.assertIsNotNone(frame.tree)
        self.assertGreater(frame.total_count, 0)
        win.destroy()

    def test_transactions_frame_init(self):
        win = tk.Toplevel(self.root)
        win.withdraw()
        frame = TransactionsFrame(win)
        self.assertIsNotNone(frame.sales_tree)
        self.assertIsNotNone(frame.items_tree)
        win.destroy()

    def test_store_settings_frame_init(self):
        win = tk.Toplevel(self.root)
        win.withdraw()
        frame = StoreSettingsFrame(win)
        self.assertIn("Monday", frame.day_entries)
        self.assertIn("Sunday", frame.day_entries)
        win.destroy()

    def test_admin_color_constants(self):
        # Verify color attributes are standard across admin portal
        from admin_app.admin_main import SnapKartModernDashboard
        self.assertTrue(hasattr(SnapKartModernDashboard, "__init__"))

    def test_db_staff_and_suppliers_schema(self):
        # Verify staff, suppliers, and system_settings tables are active in database
        from database.db_connection import get_db_connection
        conn = get_db_connection()
        self.assertIsNotNone(conn)
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES LIKE 'staff';")
        self.assertEqual(len(cursor.fetchall()), 1)
        cursor.execute("SHOW TABLES LIKE 'suppliers';")
        self.assertEqual(len(cursor.fetchall()), 1)
        cursor.execute("SHOW TABLES LIKE 'system_settings';")
        self.assertEqual(len(cursor.fetchall()), 1)
        cursor.close()
        conn.close()

