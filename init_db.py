from database import get_connection

conn = get_connection()

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
course TEXT NOT NULL,
photo TEXT DEFAULT '')
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL UNIQUE,
email TEXT NOT NULL UNIQUE,
password TEXT NOT NULL,
role TEXT NOT NULL DEFAULT 'student'
)
""")

conn.commit()
conn.close()
print("Database Created Successfully")