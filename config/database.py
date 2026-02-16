import sqlite3
import os

DB_PATH = "database/clinic.db"

def get_connection():
    """Crée et retourne une connexion à la base de données SQLite"""
    # On s'assure que le dossier database existe
    if not os.path.exists("database"):
        os.makedirs("database")
        
    conn = sqlite3.connect(DB_PATH)
    # Ceci permet de récupérer les résultats sous forme de dictionnaire si besoin
    # conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    """Initialise la base de données avec le script migrations.sql"""
    conn = get_connection()
    cursor = conn.cursor()

    # Lecture du fichier migrations.sql
    # (Assure-toi que ce fichier ne contient PLUS les ALTER TABLE qui faisaient planter)
    if os.path.exists('database/migrations.sql'):
        with open('database/migrations.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        cursor.executescript(sql_script)

    # Ajout sécurisé des colonnes pour ton PFE
    cols_to_add = [
        ("poids", "TEXT"),
        ("tension", "TEXT"),
        ("img_clinique", "TEXT"),
        ("img_biologique", "TEXT"),
        ("img_radiologique", "TEXT")
    ]

    for col_name, col_type in cols_to_add:
        try:
            cursor.execute(f"ALTER TABLE consultations ADD COLUMN {col_name} {col_type}")
        except sqlite3.OperationalError:
            pass # La colonne existe déjà

    conn.commit()
    conn.close()