from PyQt6.QtCore import QDate
from models.suivi_model import SuiviModel

def add_suivi(data):
    data["date_suivi"] = QDate.currentDate().toString("yyyy-MM-dd")
    SuiviModel.create(data)

def get_suivis(pid):
    return SuiviModel.get_by_patient(pid)
