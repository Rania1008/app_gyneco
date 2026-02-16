from models.consultation_model import ConsultationModel
from PyQt6.QtCore import QDate

def get_consultations(patient_id):
    return ConsultationModel.get_by_patient(patient_id)

def add_consultation(data):
    """Insère une nouvelle consultation en base de données"""
    # On s'assure d'avoir une date si elle n'est pas fournie
    if "date_consultation" not in data:
        data["date_consultation"] = QDate.currentDate().toString("yyyy-MM-dd")
    
    return ConsultationModel.insert(data)