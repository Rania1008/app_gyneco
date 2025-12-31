import sqlite3

DB_PATH = "database/clinic.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    with open("database/migrations.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
