from config.database import get_connection


class RendezVousModel:

    @staticmethod
    def create(data):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO rendez_vous (
                patient_id, date_rdv, heure_rdv, statut
            ) VALUES (?, ?, ?, ?)
        """, (
            data["patient_id"],
            data["date_rdv"],
            data["heure_rdv"],
            data["statut"]
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def update(rdv_id, data):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE rendez_vous
            SET date_rdv=?, heure_rdv=?, statut=?
            WHERE id=?
        """, (
            data["date_rdv"],
            data["heure_rdv"],
            data["statut"],
            rdv_id
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(rdv_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM rendez_vous WHERE id=?", (rdv_id,)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT r.id, p.nom, r.date_rdv, r.heure_rdv, r.statut
            FROM rendez_vous r
            JOIN patients p ON p.id = r.patient_id
            ORDER BY r.date_rdv, r.heure_rdv
        """)
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_today():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT r.heure_rdv, p.nom, r.statut
            FROM rendez_vous r
            JOIN patients p ON p.id = r.patient_id
            WHERE r.date_rdv = DATE('now')
            ORDER BY r.heure_rdv
        """)
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_all_dates():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT date_rdv FROM rendez_vous
        """)
        rows = cur.fetchall()
        conn.close()
        return [r[0] for r in rows]

    @staticmethod
    def get_by_date(date_str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT r.heure_rdv, p.nom, r.statut
            FROM rendez_vous r
            JOIN patients p ON p.id = r.patient_id
            WHERE r.date_rdv = ?
            ORDER BY r.heure_rdv
        """, (date_str,))
        rows = cur.fetchall()
        conn.close()
        return rows
