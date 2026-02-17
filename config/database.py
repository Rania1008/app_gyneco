import sqlite3
import os

DB_PATH = "database/clinic.db"

def get_connection():
    if not os.path.exists("database"):
        os.makedirs("database")
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Initialisation via migrations.sql
    if os.path.exists('database/migrations.sql'):
        with open('database/migrations.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        cursor.executescript(sql_script)

    # Ajout sécurisé des colonnes manquantes
    cols_to_add = [
        ("poids", "TEXT"), ("tension", "TEXT"),
        ("img_clinique", "TEXT"), ("img_biologique", "TEXT"), ("img_radiologique", "TEXT")
    ]

    for col_name, col_type in cols_to_add:
        try:
            cursor.execute(f"ALTER TABLE consultations ADD COLUMN {col_name} {col_type}")
        except sqlite3.OperationalError:
            pass 

    conn.commit()
    conn.close()