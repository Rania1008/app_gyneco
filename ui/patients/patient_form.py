from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QTextEdit,
    QComboBox, QDateEdit, QPushButton, QMessageBox, QLabel
)
from PyQt6.QtCore import QDate
from datetime import date
from services.patient_service import create_patient, update_patient

class PatientForm(QWidget):
    def __init__(self, refresh_callback, patient=None):
        super().__init__()
        self.refresh_callback = refresh_callback
        self.patient = patient
        self.setWindowTitle("Fiche Patient")
        self.resize(400, 500)
        self.setup_ui()
        if self.patient:
            self.fill_form()

    def setup_ui(self):
        layout = QFormLayout()
        self.nom = QLineEdit()
        self.telephone = QLineEdit()
        self.adresse = QTextEdit()
        
        # Section Date de naissance et Âge
        self.date_naissance = QDateEdit()
        self.date_naissance.setCalendarPopup(True)
        self.date_naissance.setDate(QDate.currentDate().addYears(-25)) # Par défaut 25 ans
        self.date_naissance.dateChanged.connect(self.update_age_display)
        
        self.age_display = QLabel("Âge : -- ans")
        self.age_display.setStyleSheet("font-weight: bold; color: #3498db;")

        self.situation = QComboBox()
        self.situation.addItems(["Célibataire", "Mariée", "Divorcée", "Veuve"])

        self.assurance = QComboBox()
        self.assurance.addItems(["CNSS", "CNOPS", "AMO", "Privée", "Aucune"])

        self.save_btn = QPushButton("💾 Enregistrer")
        self.save_btn.clicked.connect(self.save)

        layout.addRow("Nom *", self.nom)
        layout.addRow("Téléphone", self.telephone)
        layout.addRow("Adresse", self.adresse)
        layout.addRow("Date de naissance", self.date_naissance)
        layout.addRow("", self.age_display)
        layout.addRow("Situation familiale", self.situation)
        layout.addRow("Assurance", self.assurance)
        layout.addRow(self.save_btn)
        self.setLayout(layout)
        self.update_age_display(self.date_naissance.date())

    def update_age_display(self, qdate):
        today = date.today()
        birth = qdate.toPyDate()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        self.age_display.setText(f"Âge : {age} ans")

    def fill_form(self):
        self.nom.setText(self.patient["nom"])
        self.telephone.setText(self.patient.get("telephone", ""))
        self.adresse.setText(self.patient.get("adresse", ""))
        dn = self.patient.get("date_naissance")
        if dn:
            self.date_naissance.setDate(QDate.fromString(dn, "yyyy-MM-dd"))
        self.situation.setCurrentText(self.patient.get("situation_familiale", "Célibataire"))
        self.assurance.setCurrentText(self.patient.get("assurance", "Aucune"))

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
        if self.patient:
            update_patient(self.patient["id"], data)
        else:
            create_patient(data)
        self.refresh_callback()
        self.close()