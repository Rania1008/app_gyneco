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

    # 1. Création des tables de base si elles n'existent pas
    if os.path.exists('database/migrations.sql'):
        with open('database/migrations.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        cursor.executescript(sql_script)

    # 2. Mise à jour de la structure (Migrations forcées)
    # Liste des colonnes à vérifier dans la table consultations
    consult_cols = [
        ("poids", "TEXT"),
        ("tension", "TEXT"),
        ("img_clinique", "TEXT"),
        ("img_biologique", "TEXT"),
        ("img_radiologique", "TEXT"),
        ("filename", "TEXT")  # <--- C'est cette colonne qui cause l'erreur
    ]

    for col_name, col_type in consult_cols:
        try:
            cursor.execute(f"ALTER TABLE consultations ADD COLUMN {col_name} {col_type}")
        except sqlite3.OperationalError:
            # La colonne existe déjà, on passe à la suivante
            pass

    # 3. Vérification pour la table factures (pour la secrétaire)
    try:
        cursor.execute("ALTER TABLE factures ADD COLUMN notes TEXT")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()