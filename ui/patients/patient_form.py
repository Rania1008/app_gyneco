from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit,
    QComboBox, QDateEdit, QPushButton,
    QFormLayout, QMessageBox
)
from PyQt6.QtCore import QDate
from services.patient_service import create_patient

class PatientForm(QWidget):

    def __init__(self, refresh_callback=None):
        super().__init__()
        self.refresh_callback = refresh_callback
        self.setWindowTitle("Nouveau patient")
        self.setup_ui()

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

        save_btn = QPushButton("Enregistrer")
        save_btn.clicked.connect(self.save)

        layout.addRow("Nom :", self.nom)
        layout.addRow("Téléphone :", self.telephone)
        layout.addRow("Adresse :", self.adresse)
        layout.addRow("Date de naissance :", self.date_naissance)
        layout.addRow("Situation familiale :", self.situation)
        layout.addRow("Assurance :", self.assurance)
        layout.addRow(save_btn)

        self.setLayout(layout)

    def save(self):
        if not self.nom.text().strip():
            QMessageBox.warning(self, "Erreur", "Le nom est obligatoire")
            return

        data = {
            "nom": self.nom.text(),
            "telephone": self.telephone.text(),
            "adresse": self.adresse.toPlainText(),
            "date_naissance": self.date_naissance.date().toString("yyyy-MM-dd"),
            "situation_familiale": self.situation.currentText(),
            "assurance": self.assurance.currentText()
        }

        create_patient(data)
        QMessageBox.information(self, "Succès", "Patient enregistré")

        if self.refresh_callback:
            self.refresh_callback()

        self.close()
