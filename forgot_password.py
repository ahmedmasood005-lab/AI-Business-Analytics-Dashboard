import sqlite3
import bcrypt

def reset_password(username, new_password):

    conn = sqlite3.connect("analytics.db")
    cursor = conn.cursor()

    # Check if the user exists
    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()

    if user is None:
        conn.close()
        return False

    # Hash the new password
    hashed_password = bcrypt.hashpw(
        new_password.encode("utf-8"),
        bcrypt.gensalt()
    )

    # Update the password
    cursor.execute(
        "UPDATE users SET password=? WHERE username=?",
        (hashed_password, username)
    )

    conn.commit()
    conn.close()

    return True