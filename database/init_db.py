import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'airline.db')
INIT_SCRIPT = os.path.join(os.path.dirname(__file__), 'init.sql')

print(f"Using DB at: {DB_PATH}")

if not os.path.exists(INIT_SCRIPT):
    print("❌ init.sql file not found.")
else:
    with open(INIT_SCRIPT, 'r') as f:
        sql_script = f.read()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")
