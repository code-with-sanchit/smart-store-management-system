import hashlib
import hmac
import secrets
from database.db_connection import get_db_connection


def hash_password(password: str) -> str:
    """Return a salted password hash suitable for the local customer table."""
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("ascii"), 260_000)
    return f"pbkdf2_sha256${salt}${digest.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Check modern hashes and retain sign-in access for legacy SHA-256 users."""
    if stored_hash.startswith("pbkdf2_sha256$"):
        try:
            _, salt, expected = stored_hash.split("$", 2)
        except ValueError:
            return False
        actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("ascii"), 260_000).hex()
        return hmac.compare_digest(actual, expected)
    return hmac.compare_digest(stored_hash, hashlib.sha256(password.encode("utf-8")).hexdigest())


def register_customer(full_name: str, email: str, phone: str, password: str):
    """
    Registers a new customer in MySQL.
    Returns: (success: bool, message: str)
    """
    if not full_name or not email or not phone or not password:
        return False, "All fields are required!"

    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    # Basic email validation
    if "@" not in email or "." not in email.split("@")[-1]:
        return False, "Please enter a valid email address."

    # Basic phone validation
    phone_digits = ''.join(c for c in phone if c.isdigit())
    if len(phone_digits) < 10:
        return False, "Phone number must have at least 10 digits."

    conn = get_db_connection()
    if not conn:
        return False, "Database connection failed."

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)

        # Check if email is already taken
        cursor.execute("SELECT customer_id FROM customers WHERE email = %s", (email.lower().strip(),))
        if cursor.fetchone():
            return False, "An account with this email already exists."

        # Insert new customer with hashed password
        pwd_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO customers (full_name, email, phone, password_hash)
            VALUES (%s, %s, %s, %s)
        """, (full_name.strip(), email.lower().strip(), phone.strip(), pwd_hash))

        conn.commit()
        return True, "Account created successfully! You can now log in."

    except Exception as e:
        return False, f"Registration failed: {e}"
    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                pass
        if conn and conn.is_connected():
            conn.close()


def login_customer(email: str, password: str):
    """
    Checks email and password against the MySQL database.
    Returns: (success: bool, user_dict_or_None, message: str)
    """
    if not email or not password:
        return False, None, "Please enter both email and password."

    conn = get_db_connection()
    if not conn:
        return False, None, "Database connection failed."

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT customer_id, full_name, email, phone, password_hash 
            FROM customers 
            WHERE email = %s
        """, (email.lower().strip(),))

        user = cursor.fetchone()

        if not user:
            return False, None, "No account found with this email."

        # Compare password hash
        if not verify_password(password, user["password_hash"]):
            return False, None, "Incorrect password. Please try again."

        if not user["password_hash"].startswith("pbkdf2_sha256$"):
            cursor.execute(
                "UPDATE customers SET password_hash = %s WHERE customer_id = %s",
                (hash_password(password), user["customer_id"])
            )
            conn.commit()

        # Return user details without the password hash
        del user["password_hash"]
        return True, user, f"Welcome back, {user['full_name']}!"

    except Exception as e:
        return False, None, f"Login failed: {e}"
    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Exception:
                pass
        if conn and conn.is_connected():
            conn.close()
