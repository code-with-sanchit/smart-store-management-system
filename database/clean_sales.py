import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.db_connection import get_db_connection


def remove_dummy_sales():
    conn = get_db_connection()
    if not conn:
        print("Database connection failed.")
        return

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("DELETE FROM sale_items;")
        cursor.execute("DELETE FROM sales;")
        cursor.execute("DELETE FROM customers;")
        cursor.execute("ALTER TABLE sales AUTO_INCREMENT = 1;")
        cursor.execute("ALTER TABLE sale_items AUTO_INCREMENT = 1;")
        cursor.execute("ALTER TABLE customers AUTO_INCREMENT = 1;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        conn.commit()
        print("Successfully wiped all sales and customer records! Database is clean.")
    except Exception as e:
        print(f"Error during cleanup: {e}")
    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                pass
        if conn and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    remove_dummy_sales()