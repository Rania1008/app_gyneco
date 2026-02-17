from config.database import get_connection

class ConsultationModel:
    @staticmethod
    def get_by_patient(patient_id):
        conn = get_connection()
        cursor = conn.cursor()
        # On demande les 4 colonnes : id(0), date(1), motif(2), filename(3)
        cursor.execute("""
            SELECT id, date_consultation, motif_consultation, filename 
            FROM consultations WHERE patient_id = ? 
            ORDER BY id DESC
        """, (patient_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def insert(data):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO consultations (
                patient_id, date_consultation, motif_consultation, filename,
                poids, tension, examen_clinique, img_clinique, 
                img_biologique, img_radiologique
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            data['patient_id'], data['date_consultation'], data['motif'], 
            data.get('filename'), data.get('poids'), data.get('tension'),
            data.get('examen_clinique'), data.get('img_clinique'),
            data.get('img_biologique'), data.get('img_radiologique')
        ))
        conn.commit()
        conn.close()