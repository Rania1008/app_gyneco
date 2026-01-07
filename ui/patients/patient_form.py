from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QTextEdit,
    QComboBox, QDateEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import QDate
from services.patient_service import create_patient, update_patient


class PatientForm(QWidget):
    """Formulaire Ajouter / Modifier Patient"""

    def __init__(self, refresh_callback, patient=None):
        super().__init__()
        self.refresh_callback = refresh_callback
        self.patient = patient
        self.setWindowTitle("Patient")
        self.resize(400, 450)

        self.setup_ui()

        if self.patient:
            self.fill_form()

    def setup_ui(self):
        layout = QFormLayout()

        self.nom = QLineEdit()
        self.telephone = QLineEdit()
        self.adresse = QTextEdit()

        self.date_naissance = QDateEdit()
        self.date_naissance.setCalendarPopup(True)
        self.date_naissance.setDate(QDate.currentDate())

        self.situation = QComboBox()
        self.situation.addItems([
            "Célibataire", "Mariée", "Divorcée", "Veuve"
        ])

        self.assurance = QComboBox()
        self.assurance.addItems([
            "CNSS", "CNOPS", "AMO", "Privée", "Aucune"
        ])

        self.save_btn = QPushButton("Enregistrer")
        self.save_btn.clicked.connect(self.save)

        layout.addRow("Nom *", self.nom)
        layout.addRow("Téléphone", self.telephone)
        layout.addRow("Adresse", self.adresse)
        layout.addRow("Date de naissance", self.date_naissance)
        layout.addRow("Situation familiale", self.situation)
        layout.addRow("Assurance", self.assurance)
        layout.addRow(self.save_btn)

        self.setLayout(layout)

    def fill_form(self):
        """Remplit le formulaire en mode modification"""
        self.nom.setText(self.patient.get("nom", ""))
        self.telephone.setText(self.patient.get("telephone", ""))
        self.adr
