from config.database import get_connection

class FactureModel:
    @staticmethod
    def create(data):
        conn = get_connection()
        cursor = conn.cursor()
        
        total = float(data.get('total', 0))
        paye = float(data.get('paye', 0))
        reste = total - paye
        
        query = """
            INSERT INTO factures (
                patient_id, reference, date_facture, total, paye, reste, notes
            ) VALUES (?, ?, DATE('now'), ?, ?, ?, ?)
        """
        cursor.execute(query, (
            data['patient_id'], data['reference'], 
            total, paye, reste, data.get('notes')
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_factures():
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT f.id, f.reference, p.nom, f.date_facture, f.total, f.paye, f.reste
            FROM factures f
            JOIN patients p ON f.patient_id = p.id
            ORDER BY f.id DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_list_patients():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nom FROM patients ORDER BY nom")
        rows = cursor.fetchall()
        conn.close()
        return rows