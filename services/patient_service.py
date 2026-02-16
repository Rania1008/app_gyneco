from PyQt6.QtCore import QDate
from models.patient_model import PatientModel

def create_patient(data):
    today = QDate.currentDate().toString("yyyy-MM-dd")
    data["date_premiere_consultation"] = today
    data["created_at"] = today
    PatientModel.insert(data)

def update_patient(patient_id, data):
    PatientModel.update(patient_id, data)

def delete_patient(patient_id):
    PatientModel.delete(patient_id)

def get_patients():
    return PatientModel.get_all()

def get_patient_by_id(patient_id):
    """Récupère un patient et le transforme en dictionnaire pour le formulaire"""
    data = PatientModel.get_by_id(patient_id)
    if data:
        # On assume l'ordre : ID, Nom, Tel, Adresse, Naissance, Situation, Assurance, ...
        return {
            "id": data[0],
            "nom": data[1],
            "telephone": data[2],
            "adresse": data[3],
            "date_naissance": data[4],
            "situation_familiale": data[5],
            "assurance": data[6]
        }
    return None