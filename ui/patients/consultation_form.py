import os
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QFormLayout, QLineEdit, QTextEdit, 
                             QPushButton, QFileDialog, QVBoxLayout, QMessageBox)
from services.consultation_service import add_consultation
from utils.pdf_consultation import export_consultation_pdf

class ConsultationForm(QWidget):
    def __init__(self, patient_data, refresh_callback):
        super().__init__()
        self.patient = patient_data
        self.refresh_callback = refresh_callback
        self.photos = {"clinique": None, "biologique": None, "radiologique": None}
        self.setWindowTitle(f"Nouvelle Consultation - {self.patient['nom']}")
        self.resize(500, 800)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.motif = QLineEdit()
        self.antecedants = QTextEdit()
        self.poids = QLineEdit()
        self.tension = QLineEdit()
        self.clinique = QTextEdit()
        self.biologique = QTextEdit()
        self.radio = QTextEdit()
        self.diag = QTextEdit()
        self.traitement = QTextEdit()

        form.addRow("Motif *", self.motif)
        form.addRow("Antécédents", self.antecedants)
        form.addRow("Poids (kg)", self.poids)
        form.addRow("Tension", self.tension)
        form.addRow("Examen Clinique", self.clinique)
        form.addRow("Examen Biologique", self.biologique)
        form.addRow("Examen Radiologique", self.radio)
        form.addRow("Diagnostique", self.diag)
        form.addRow("Traitement", self.traitement)

        btn_save = QPushButton("💾 Enregistrer & Générer PDF")
        btn_save.setStyleSheet("background-color: #2ecc71; color: white; height: 40px; font-weight: bold;")
        btn_save.clicked.connect(self.save_consultation)
        
        layout.addLayout(form)
        layout.addWidget(btn_save)

    def save_consultation(self):
        if not self.motif.text().strip():
            QMessageBox.warning(self, "Erreur", "Le motif est obligatoire.")
            return

        date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Création du dossier exports s'il n'existe pas
        if not os.path.exists("exports"): 
            os.makedirs("exports")
        
        # NOM DU FICHIER : IMPORTANT POUR LA SYNCHRONISATION
        pdf_name = f"exports/consult_{self.patient['id']}_{date_str}.pdf"
        
        data = {
            "patient_id": self.patient['id'],
            "date_consultation": date_str,
            "motif": self.motif.text(),
            "antecedants": self.antecedants.toPlainText(),
            "poids": self.poids.text(),
            "tension": self.tension.text(),
            "examen_clinique": self.clinique.toPlainText(),
            "examen_biologique": self.biologique.toPlainText(),
            "examen_radiologique": self.radio.toPlainText(),
            "diagnostique": self.diag.toPlainText(),
            "traitement": self.traitement.toPlainText()
        }

        # Calcul de l'âge pour le PDF
        try:
            dob = datetime.strptime(self.patient['date_naissance'], "%Y-%m-%d")
            age = datetime.now().year - dob.year
        except:
            age = "N/A"

        # Export PDF
        export_consultation_pdf(pdf_name, self.patient['nom'], age, date_str, data)
        # Sauvegarde Base de données
        add_consultation(data)
        
        QMessageBox.information(self, "Succès", "Consultation et PDF enregistrés !")
        self.refresh_callback()
        self.close()