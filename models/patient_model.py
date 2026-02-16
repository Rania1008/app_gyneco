from config.database import get_connection

class PatientModel:
    @staticmethod
    def get_all():
        """Récupère tous les patients pour le tableau principal"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nom, telephone, assurance, date_premiere_consultation FROM patients")
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_by_id(patient_id):
        """
        Récupère TOUTES les colonnes d'un patient spécifique.
        C'est cette méthode qui manquait dans votre erreur.
        """
        conn = get_connection()
        cursor = conn.cursor()
        # Assurez-vous que l'ordre des colonnes correspond à ce que get_patient_by_id attend
        cursor.execute("""
            SELECT id, nom, telephone, adresse, date_naissance, situation_familiale, assurance 
            FROM patients 
            WHERE id = ?
        """, (patient_id,))
        row = cursor.fetchone()
        conn.close()
        return row

    @staticmethod
    def insert(data):
        """Insère un nouveau patient"""
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO patients (nom, telephone, adresse, date_naissance, situation_familiale, assurance, date_premiere_consultation, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            data['nom'], data['telephone'], data['adresse'], 
            data['date_naissance'], data['situation_familiale'], 
            data['assurance'], data['date_premiere_consultation'], data['created_at']
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def update(patient_id, data):
        """Met à jour les informations d'un patient"""
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE patients 
            SET nom=?, telephone=?, adresse=?, date_naissance=?, situation_familiale=?, assurance=?
            WHERE id=?
        """
        cursor.execute(query, (
            data['nom'], data['telephone'], data['adresse'], 
            data['date_naissance'], data['situation_familiale'], 
            data['assurance'], patient_id
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(patient_id):
        """Supprime un patient"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
        conn.commit()
        conn.close()