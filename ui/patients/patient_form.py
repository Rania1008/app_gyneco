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
        """Mode modification"""
        self.nom.setText(self.patient["nom"])
        self.telephone.setText(self.patient.get("telephone", ""))
        self.adresse.setText(self.patient.get("adresse", ""))
        self.date_naissance.setDate(
            QDate.fromString(
                self.patient.get("date_naissance", QDate.currentDate().toString("yyyy-MM-dd")),
                "yyyy-MM-dd"
            )
        )
        self.situation.setCurrentText(
            self.patient.get("situation_familiale", "Célibataire")
        )
        self.assurance.setCurrentText(
            self.patient.get("assurance", "Aucune")
        )

    # ==================================================
    # ✅ MÉTHODE MANQUANTE → BUG RÉGLÉ
    # ==================================================
    def save(self):
        if not self.nom.text().strip():
            QMessageBox.warning(
                self, "Erreur", "Le nom est obligatoire"
            )
            return

        data = {
            "nom": self.nom.text(),
            "telephone": self.telephone.text(),
            "adresse": self.adresse.toPlainText(),
            "date_naissance": self.date_naissance.date().toString("yyyy-MM-dd"),
            "situation_familiale": self.situation.currentText(),
            "assurance": self.assurance.currentText()
        }

        if self.patient:
            update_patient(self.patient["id"], data)
        else:
            create_patient(data)

        self.refresh_callback()
        self.close()
