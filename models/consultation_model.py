from config.database import get_connection

class ConsultationModel:

    @staticmethod
    def create(data):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO consultations (
                patient_id, date_consultation,
                antecedants, motif_consultation,
                examen_clinique, examen_biologique,
                examen_radiologique, diagnostique, traitement
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["patient_id"], data["date_consultation"],
            data["antecedants"], data["motif_consultation"],
            data["examen_clinique"], data["examen_biologique"],
            data["examen_radiologique"], data["diagnostique"],
            data["traitement"]
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def update(cid, data):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE consultations SET
                antecedants=?, motif_consultation=?,
                examen_clinique=?, examen_biologique=?,
                examen_radiologique=?, diagnostique=?, traitement=?
            WHERE id=?
        """, (
            data["antecedants"], data["motif_consultation"],
            data["examen_clinique"], data["examen_biologique"],
            data["examen_radiologique"], data["diagnostique"],
            data["traitement"], cid
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_patient(pid):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM consultations
            WHERE patient_id=?
            ORDER BY date_consultation DESC
        """, (pid,))
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def delete(cid):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM consultations WHERE id=?", (cid,))
        conn.commit()
        conn.close()
