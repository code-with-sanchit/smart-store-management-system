import os
from pathlib import Path

import mysql.connector
from mysql.connector import Error, pooling

# Look for .env in project root and load key-values into os.environ if not already present
def _load_dotenv():
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if not env_file.is_file():
        return
    try:
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k and k not in os.environ:
                    os.environ[k] = v
    except Exception:
        pass

_load_dotenv()

DB_CONFIG = {
    'host': os.environ.get('SNAPKART_DB_HOST', 'localhost'),
    'user': os.environ.get('SNAPKART_DB_USER', 'root'),
    'password': os.environ.get('SNAPKART_DB_PASSWORD', 'Sanc@2007'),
    'database': os.environ.get('SNAPKART_DB_NAME', 'smart_store_db'),
    'autocommit': False,
    'connection_timeout': 5,
    'pool_name': 'snapkart_pool',
    'pool_size': 5,
}

_pool = None


def _get_pool():
    """Create the small shared connection pool on first use."""
    global _pool
    if _pool is None:
        _load_dotenv()
        DB_CONFIG['host'] = os.environ.get('SNAPKART_DB_HOST', DB_CONFIG['host'])
        DB_CONFIG['user'] = os.environ.get('SNAPKART_DB_USER', DB_CONFIG['user'])
        DB_CONFIG['password'] = os.environ.get('SNAPKART_DB_PASSWORD', DB_CONFIG['password'])
        DB_CONFIG['database'] = os.environ.get('SNAPKART_DB_NAME', DB_CONFIG['database'])
        _pool = pooling.MySQLConnectionPool(**DB_CONFIG)
    return _pool


def get_db_connection():
    """
    Returns a new MySQL connection using config from environment or defaults.
    Callers must close the connection when done.
    Returns None if connection fails.
    """
    try:
        connection = _get_pool().get_connection()
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return None


def ensure_core_schema():
    """
    Ensures all required columns and constraints exist across tables.
    Safe to call multiple times; uses IF NOT EXISTS / information_schema checks.
    """
    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor(dictionary=True)
        db_name = DB_CONFIG['database']

        # Ensure customers table exists with VARCHAR(255) password_hash
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(120) NOT NULL,
            email VARCHAR(120) NOT NULL UNIQUE,
            phone VARCHAR(20) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Upgrade password_hash column if existing table had VARCHAR(64)
        cursor.execute("""
            SELECT CHARACTER_MAXIMUM_LENGTH
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = %s
              AND TABLE_NAME = 'customers'
              AND COLUMN_NAME = 'password_hash';
        """, (db_name,))
        pwd_col = cursor.fetchone()
        if pwd_col and (pwd_col.get("CHARACTER_MAXIMUM_LENGTH") or 0) < 255:
            cursor.execute("ALTER TABLE customers MODIFY COLUMN password_hash VARCHAR(255) NOT NULL;")

        # Ensure payment_method column exists on sales
        cursor.execute("""
            SELECT COUNT(*) AS col_exists
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = %s
              AND TABLE_NAME = 'sales'
              AND COLUMN_NAME = 'payment_method';
        """, (db_name,))
        if cursor.fetchone()["col_exists"] == 0:
            cursor.execute("ALTER TABLE sales ADD COLUMN payment_method VARCHAR(50) DEFAULT 'Cash';")
        else:
            cursor.execute("ALTER TABLE sales MODIFY COLUMN payment_method VARCHAR(50) DEFAULT 'Cash';")

        # Ensure customer_id column exists on sales
        cursor.execute("""
            SELECT COUNT(*) AS col_exists
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = %s
              AND TABLE_NAME = 'sales'
              AND COLUMN_NAME = 'customer_id';
        """, (db_name,))
        if cursor.fetchone()["col_exists"] == 0:
            cursor.execute("ALTER TABLE sales ADD COLUMN customer_id INT NULL;")

        # Ensure FK constraint (ignore if it already exists)
        try:
            cursor.execute("""
                SELECT COUNT(*) AS fk_exists
                FROM information_schema.TABLE_CONSTRAINTS
                WHERE TABLE_SCHEMA = %s
                  AND TABLE_NAME = 'sales'
                  AND CONSTRAINT_NAME = 'fk_sales_customer';
            """, (db_name,))
            if cursor.fetchone()["fk_exists"] == 0:
                cursor.execute("""
                    ALTER TABLE sales
                    ADD CONSTRAINT fk_sales_customer
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                    ON DELETE SET NULL;
                """)
        except Exception:
            pass  # FK might already exist under different name

        # Indexes for fast catalog browsing and analytics
        for statement in (
            "CREATE INDEX idx_catalog_category_stock ON inventory (category, stock_quantity, item_id)",
            "CREATE INDEX idx_catalog_stock_item ON inventory (stock_quantity, item_id)",
            "CREATE INDEX idx_sales_date_amount ON sales (sale_datetime, total_amount)",
        ):
            try:
                cursor.execute(statement)
            except Error:
                pass

        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Schema migration notice: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()
