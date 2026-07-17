import sqlite3
import bcrypt

def register_user(username, password):

    conn = sqlite3.connect("analytics.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password BLOB
    )
    """)

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    try:
        cursor.execute(
            "INSERT INTO users(username, password) VALUES(?, ?)",
            (username, hashed_password)
        )

        conn.commit()

    finally:
        conn.close()