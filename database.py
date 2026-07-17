import sqlite3
import pandas as pd
import os

# -----------------------------
# Database Name
# -----------------------------
DATABASE_NAME = "analytics.db"

# -----------------------------
# CSV File Path
# -----------------------------
CSV_FILE = "data/sales.csv"

# -----------------------------
# Check if CSV Exists
# -----------------------------
if not os.path.exists(CSV_FILE):
    print(f"Error: '{CSV_FILE}' not found.")
    exit()

# -----------------------------
# Read CSV
# -----------------------------
df = pd.read_csv(CSV_FILE)

# -----------------------------
# Calculate Total Sales
# -----------------------------
df["Total"] = df["Quantity"] * df["Price"]

# -----------------------------
# Create SQLite Database
# -----------------------------
conn = sqlite3.connect(DATABASE_NAME)

# Create sales table
df.to_sql(
    "sales",
    conn,
    if_exists="replace",
    index=False
)

# -----------------------------
# Verify Table
# -----------------------------
cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table';
""")

print("Tables in Database:")
print(cursor.fetchall())

# -----------------------------
# Verify Data
# -----------------------------
cursor.execute("SELECT COUNT(*) FROM sales")

rows = cursor.fetchone()[0]

print(f"Total Records: {rows}")

conn.commit()
conn.close()

print("\nDatabase Created Successfully!")
print(f"Database File: {DATABASE_NAME}")