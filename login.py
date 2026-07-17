import sqlite3
import bcrypt


def authenticate(username, password):
    """
    Authenticate a user from the SQLite database.
    Returns True if credentials are correct.
    """

    conn = sqlite3.connect("analytics.db")
    cursor = conn.cursor()

    # Create users table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password BLOB
        )
    """)

    # Find user
    cursor.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    # User not found
    if user is None:
        return False

    stored_password = user[0]

    # Convert stored password to bytes if needed
    if isinstance(stored_password, str):
        stored_password = stored_password.encode("utf-8")

    return bcrypt.checkpw(
        password.encode("utf-8"),
        stored_password
    )