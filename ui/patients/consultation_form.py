import os
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QFormLayout, QLineEdit, QTextEdit, 
                             QPushButton, QFileDialog, QVBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt
from services.consultation_service import add_consultation
from utils.pdf_consultation import export_consultation_pdf

class ConsultationForm(QWidget):
    def __init__(self, patient_data, refresh_callback):
        super().__init__()
        self.patient = patient_data
        self.refresh_callback = refresh_callback
        self.photos = {"clinique": None, "biologique": None, "radiologique": None}
        self.setWindowTitle(f"Nouvelle Consultation - {self.patient['nom']}")
        self.resize(550, 850)
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
        form.addRow("", self.create_img_btn("clinique"))
        
        form.addRow("Examen Biologique", self.biologique)
        form.addRow("", self.create_img_btn("biologique"))
        
        form.addRow("Examen Radiologique", self.radio)
        form.addRow("", self.create_img_btn("radiologique"))
        
        form.addRow("Diagnostique", self.diag)
        form.addRow("Traitement", self.traitement)

        btn_save = QPushButton("💾 Enregistrer & Générer PDF")
        btn_save.setStyleSheet("background-color: #2ecc71; color: white; height: 45px; font-weight: bold;")
        btn_save.clicked.connect(self.save_consultation)
        
        layout.addLayout(form)
        layout.addWidget(btn_save)

    def create_img_btn(self, key):
        btn = QPushButton(f"📎 Joindre photo {key}")
        btn.clicked.connect(lambda: self.select_image(key, btn))
        return btn

    def select_image(self, key, btn):
        path, _ = QFileDialog.getOpenFileName(self, "Choisir Image", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.photos[key] = path
            btn.setText(f"✅ Photo {key} ajoutée")
            btn.setStyleSheet("color: #27ae60; font-weight: bold;")

    def save_consultation(self):
        if not self.motif.text().strip():
            QMessageBox.warning(self, "Erreur", "Le motif est obligatoire.")
            return

        date_str = datetime.now().strftime("%Y-%m-%d")
        pdf_name = f"exports/consult_{self.patient['id']}_{date_str}.pdf"
        
        data = {
            "patient_id": self.patient['id'], "date_consultation": date_str,
            "motif": self.motif.text(), "antecedants": self.antecedants.toPlainText(),
            "poids": self.poids.text(), "tension": self.tension.text(),
            "examen_clinique": self.clinique.toPlainText(), "examen_biologique": self.biologique.toPlainText(),
            "examen_radiologique": self.radio.toPlainText(), "diagnostique": self.diag.toPlainText(),
            "traitement": self.traitement.toPlainText(),
            "img_clinique": self.photos['clinique'], "img_biologique": self.photos['biologique'], "img_radiologique": self.photos['radiologique']
        }

        # PDF Export
        sections_pdf = {k.capitalize(): v for k, v in data.items() if isinstance(v, str) and k != 'date_consultation'}
        export_consultation_pdf(pdf_name, self.patient['nom'], "N/A", date_str, sections_pdf, self.photos)
        
        add_consultation(data)
        QMessageBox.information(self, "Succès", "Enregistré avec succès !")
        self.refresh_callback()
        self.close()