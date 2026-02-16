from config.database import get_connection

class ConsultationModel:
    @staticmethod
    def insert(data):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO consultations (
                patient_id, date_consultation, motif_consultation, antecedants, 
                poids, tension, examen_clinique, examen_biologique, 
                examen_radiologique, diagnostique, traitement,
                img_clinique, img_biologique, img_radiologique
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            data['patient_id'], data['date_consultation'], data['motif'], 
            data.get('antecedants'), data.get('poids'), data.get('tension'),
            data.get('examen_clinique'), data.get('examen_biologique'),
            data.get('examen_radiologique'), data.get('diagnostique'),
            data.get('traitement'), data.get('img_clinique'),
            data.get('img_biologique'), data.get('img_radiologique')
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_patient(patient_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, date_consultation, motif_consultation 
            FROM consultations WHERE patient_id = ? 
            ORDER BY date_consultation DESC
        """, (patient_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows