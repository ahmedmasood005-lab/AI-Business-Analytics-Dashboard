import sqlite3

conn = sqlite3.connect("analytics.db")
cursor = conn.cursor()

# Check if users table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# Check users
try:
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    print("\nUsers Table:")
    print(users)

except Exception as e:
    print(e)

conn.close()