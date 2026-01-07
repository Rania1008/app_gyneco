from config.database import get_connection

class SuiviModel:

    @staticmethod
    def create(data):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO suivi_patient (
                patient_id, date_suivi,
                evolution_clinique, examen_biologique,
                examen_radiologique, traitement
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["patient_id"], data["date_suivi"],
            data["evolution_clinique"], data["examen_biologique"],
            data["examen_radiologique"], data["traitement"]
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_patient(pid):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM suivi_patient
            WHERE patient_id=?
            ORDER BY date_suivi DESC
        """, (pid,))
        rows = cur.fetchall()
        conn.close()
        return rows
