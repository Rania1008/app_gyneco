from config.database import get_connection


class PatientModel:

    @staticmethod
    def insert(data):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO patients (
                nom, telephone, adresse,
                date_naissance, situation_familiale,
                assurance, date_premiere_consultation, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["nom"], data["telephone"], data["adresse"],
            data["date_naissance"], data["situation_familiale"],
            data["assurance"], data["date_premiere_consultation"],
            data["created_at"]
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def update(patient_id, data):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE patients SET
                nom = ?, telephone = ?, adresse = ?,
                date_naissance = ?, situation_familiale = ?,
                assurance = ?
            WHERE id = ?
        """, (
            data["nom"], data["telephone"], data["adresse"],
            data["date_naissance"], data["situation_familiale"],
            data["assurance"], patient_id
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(patient_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM patients WHERE id = ?", (patient_id,)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nom, telephone, assurance, date_premiere_consultation
            FROM patients
            ORDER BY id DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows
