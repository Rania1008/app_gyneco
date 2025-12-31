from PyQt6.QtCore import QDate
from models.patient_model import PatientModel

def create_patient(data):
    # dates automatiques
    today = QDate.currentDate().toString("yyyy-MM-dd")
    data["date_premiere_consultation"] = today
    data["created_at"] = today

    PatientModel.insert(data)

def get_patients():
    return PatientModel.get_all()
