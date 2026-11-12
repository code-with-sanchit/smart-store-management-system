import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.db_connection import get_db_connection


def remove_dummy_sales(include_customers=False):
    """Clear sales history. Customer accounts are retained unless explicitly requested."""
    conn = get_db_connection()
    if not conn:
        print("Database connection failed.")
        return

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sale_items;")
        cursor.execute("DELETE FROM sales;")
        cursor.execute("ALTER TABLE sales AUTO_INCREMENT = 1;")
        cursor.execute("ALTER TABLE sale_items AUTO_INCREMENT = 1;")
        if include_customers:
            cursor.execute("DELETE FROM customers;")
            cursor.execute("ALTER TABLE customers AUTO_INCREMENT = 1;")
        conn.commit()
        print("Sales history cleared." + (" Customer accounts were also removed." if include_customers else " Customer accounts were retained."))
    except Exception as e:
        conn.rollback()
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
    parser = argparse.ArgumentParser(description="Clear demo sales safely.")
    parser.add_argument("--include-customers", action="store_true", help="also delete registered customer accounts")
    args = parser.parse_args()
    remove_dummy_sales(include_customers=args.include_customers)
