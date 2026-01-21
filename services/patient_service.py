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
