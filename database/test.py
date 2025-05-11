import sqlite3
import os

# Make sure it's pointing to the same DB file
DB_PATH = os.path.join(os.path.dirname(__file__), 'airline.db')
print(f"Reading DB from: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

conn.close()
