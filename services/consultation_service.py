from PyQt6.QtCore import QDate
from models.consultation_model import ConsultationModel

def add_consultation(data):
    data["date_consultation"] = QDate.currentDate().toString("yyyy-MM-dd")
    ConsultationModel.create(data)

def update_consultation(cid, data):
    ConsultationModel.update(cid, data)

def get_consultations(pid):
    return ConsultationModel.get_by_patient(pid)

def delete_consultation(cid):
    ConsultationModel.delete(cid)
