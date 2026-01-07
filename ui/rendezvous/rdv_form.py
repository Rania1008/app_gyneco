from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QComboBox,
    QPushButton, QMessageBox,
    QDateEdit, QTimeEdit
)
from PyQt6.QtCore import QDate, QTime
from services.rendezvous_service import add_rdv, update_rdv
from services.patient_service import get_patients


class RDVForm(QWidget):

    def __init__(self, refresh_callback, rdv=None):
        super().__init__()
        self.refresh_callback = refresh_callback
        self.rdv = rdv
        self.setWindowTitle("Rendez-vous")
        self.resize(350, 250)
        self.setup_ui()

        if self.rdv:
            self.fill_form()

    def setup_ui(self):
        layout = QFormLayout(self)

        self.patient_cb = QComboBox()
        self.patients = get_patients()
        for p in self.patients:
            self.patient_cb.addItem(p[1], p[0])

        self.date_rdv = QDateEdit()
        self.date_rdv.setCalendarPopup(True)
        self.date_rdv.setDate(QDate.currentDate())

        self.heure_rdv = QTimeEdit()
        self.heure_rdv.setTime(QTime.currentTime())

        self.statut = QComboBox()
        self.statut.addItems([
            "Programmé", "En attente", "Honoré", "Annulé"
        ])

        save_btn = QPushButton("Enregistrer")
        save_btn.clicked.connect(self.save)

        layout.addRow("Patiente *", self.patient_cb)
        layout.addRow("Date *", self.date_rdv)
        layout.addRow("Heure *", self.heure_rdv)
        layout.addRow("Statut", self.statut)
        layout.addRow(save_btn)

    def fill_form(self):
        self.date_rdv.setDate(
            QDate.fromString(self.rdv[2], "yyyy-MM-dd")
        )
        self.heure_rdv.setTime(
            QTime.fromString(self.rdv[3], "HH:mm")
        )
        self.statut.setCurrentText(self.rdv[4])

    def save(self):
        if self.patient_cb.currentIndex() < 0:
            QMessageBox.warning(
                self, "Erreur", "Patiente obligatoire"
            )
            return

        data = {
            "patient_id": self.patient_cb.currentData(),
            "date_rdv": self.date_rdv.date().toString("yyyy-MM-dd"),
            "heure_rdv": self.heure_rdv.time().toString("HH:mm"),
            "statut": self.statut.currentText()
        }

        if self.rdv:
            update_rdv(self.rdv[0], data)
        else:
            add_rdv(data)

        self.refresh_callback()
        self.close()
