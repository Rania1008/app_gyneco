import os
from datetime import datetime, date
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from services.consultation_service import get_consultations

class ActionSelector(QDialog):
    def __init__(self, patient_data):
        super().__init__()
        self.patient = patient_data 
        self.setWindowTitle(f"Dossier : {self.patient['nom']}")
        self.setMinimumSize(600, 450)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Calcul de l'âge correct (Source : Date de naissance en DB)
        try:
            dob = datetime.strptime(self.patient['date_naissance'], "%Y-%m-%d")
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            age_str = f"{age} ans"
        except: 
            age_str = "N/A"

        header = QHBoxLayout()
        header.addWidget(QLabel(f"<b>{self.patient['nom'].upper()}</b> ({age_str})"))
        
        btn_consult = QPushButton("➕ Nouvelle Consultation")
        btn_consult.setStyleSheet("padding: 5px; font-weight: bold;")
        btn_consult.clicked.connect(self.accept)
        
        header.addStretch()
        header.addWidget(btn_consult)
        layout.addLayout(header)

        # Tableau
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Date", "Motif", "Fichier"])
        self.table.setColumnHidden(2, True) 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.itemDoubleClicked.connect(self.view_pdf)
        
        layout.addWidget(QLabel("<b>Historique (Double-cliquez pour ouvrir) :</b>"))
        layout.addWidget(self.table)
        
        # RESTAURATION DU BOUTON EXPORTS
        self.btn_folder = QPushButton("📂 Ouvrir le dossier des exports PDF")
        self.btn_folder.clicked.connect(self.open_exports_folder)
        layout.addWidget(self.btn_folder)
        
        self.load_history()

    def load_history(self):
        consults = get_consultations(self.patient['id'])
        self.table.setRowCount(0)
        for c in consults:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(c[1])))
            self.table.setItem(row, 1, QTableWidgetItem(str(c[2])))
            
            # Reconstruction du chemin si c[3] (filename) est vide (pour les vieux dossiers)
            file_val = c[3] if len(c) > 3 and c[3] else f"exports/consult_{self.patient['id']}_{c[1]}.pdf"
            self.table.setItem(row, 2, QTableWidgetItem(str(file_val)))

    def view_pdf(self, item):
        file_text = self.table.item(item.row(), 2).text()
        pdf_path = os.path.abspath(file_text)
        
        if os.path.exists(pdf_path):
            os.startfile(pdf_path)
        else:
            QMessageBox.warning(self, "Erreur", f"Fichier introuvable :\n{file_text}")

    def open_exports_folder(self):
        path = os.path.abspath("exports")
        if not os.path.exists(path): os.makedirs(path)
        os.startfile(path)