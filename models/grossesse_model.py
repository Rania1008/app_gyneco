from config.database import get_connection

class GrossesseModel:

    @staticmethod
    def create(data):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO grossesse (
                patient_id, date_derniere_regle,
                grossesse_precedente, fetus,
                status, a_terme_le, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data["patient_id"], data["date_derniere_regle"],
            data["grossesse_precedente"], data["fetus"],
            data["status"], data["a_terme_le"], data["notes"]
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_patient(pid):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM grossesse WHERE patient_id=?
        """, (pid,))
        rows = cur.fetchall()
        conn.close()
        return rows
