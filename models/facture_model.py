import sqlite3

class FactureModel:

    @staticmethod
    def facture_existe_pour_consultation(consultation_id, conn):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM factures WHERE consultation_id = ?",
            (consultation_id,)
        )
        return cursor.fetchone() is not None

    @staticmethod
    def creer_facture(patient_id, consultation_id, reference, total, paye, reste, conn):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO factures (
                patient_id, consultation_id, reference,
                total, paye, reste
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (patient_id, consultation_id, reference, total, paye, reste))
        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def ajouter_detail(facture_id, service, frais, conn):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO facture_details (facture_id, service, frais)
            VALUES (?, ?, ?)
        """, (facture_id, service, frais))
        conn.commit()
