import sqlite3

conn = sqlite3.connect("db.sqlite3")

cursor = conn.cursor()

try:
    cursor.execute(
        "ALTER TABLE user_progress ADD COLUMN time_taken INTEGER DEFAULT 0"
    )
    print("✅ time_taken column added")
except Exception as e:
    print("⚠️ Column may already exist:", e)

conn.commit()
conn.close()