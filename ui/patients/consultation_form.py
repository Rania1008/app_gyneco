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
        self.setWindowTitle("Nouvelle Consultation")
        self.resize(550, 850)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.motif = QLineEdit()
        self.poids = QLineEdit()
        self.tension = QLineEdit()
        self.clinique = QTextEdit()
        self.biologique = QTextEdit()
        self.radio = QTextEdit()

        form.addRow("Motif *", self.motif)
        form.addRow("Poids (kg)", self.poids)
        form.addRow("Tension", self.tension)
        form.addRow("Examen Clinique", self.clinique)
        form.addRow("", self.create_img_btn("clinique"))
        form.addRow("Examen Biologique", self.biologique)
        form.addRow("", self.create_img_btn("biologique"))
        form.addRow("Examen Radiologique", self.radio)
        form.addRow("", self.create_img_btn("radiologique"))

        btn_save = QPushButton("💾 Enregistrer & Générer PDF")
        btn_save.clicked.connect(self.save_consultation)
        layout.addLayout(form)
        layout.addWidget(btn_save)

    def create_img_btn(self, key):
        btn = QPushButton(f"📎 Joindre photo {key}")
        btn.clicked.connect(lambda: self.select_image(key, btn))
        return btn

    def select_image(self, key, btn):
        path, _ = QFileDialog.getOpenFileName(self, "Image", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.photos[key] = path
            btn.setText("✅ Photo ajoutée")

    def save_consultation(self):
        if not self.motif.text().strip():
            QMessageBox.warning(self, "Erreur", "Le motif est obligatoire.")
            return

        now = datetime.now()
        date_db = now.strftime("%Y-%m-%d")
        # On ajoute les secondes pour garantir un nom de fichier unique et éviter le PermissionError
        date_filename = now.strftime("%Y-%m-%d_%H%M%S")
        
        pdf_name = f"exports/consult_{self.patient['id']}_{date_filename}.pdf"
        
        data = {
            "patient_id": self.patient['id'], 
            "date_consultation": date_db, # Garde la date simple pour la DB
            "filename": pdf_name, # Stocke le nom exact du fichier pour le retrouver
            "motif": self.motif.text(), 
            "poids": self.poids.text(),
            "tension": self.tension.text(), 
            "examen_clinique": self.clinique.toPlainText(),
            "img_clinique": self.photos['clinique'], 
            "img_biologique": self.photos['biologique'], 
            "img_radiologique": self.photos['radiologique']
        }

        export_consultation_pdf(pdf_name, self.patient['nom'], "N/A", date_db, data, self.photos)
        add_consultation(data)
        
        QMessageBox.information(self, "Succès", "Consultation enregistrée ! Le médecin peut laisser le PDF ouvert.")
        self.refresh_callback()
        self.close()