import os
from datetime import datetime, date
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt
from services.consultation_service import get_consultations

class ActionSelector(QDialog):
    def __init__(self, patient_data):
        super().__init__()
        self.patient = patient_data
        self.setWindowTitle(f"Dossier : {self.patient['nom']}")
        self.setMinimumSize(600, 400)
        self.resultat = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # CALCUL DE L'AGE CORRIGÉ
        age_str = "Âge : Non renseigné"
        if self.patient.get('date_naissance'):
            try:
                dob = datetime.strptime(self.patient['date_naissance'], "%Y-%m-%d")
                today = date.today()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                age_str = f"Âge : {age} ans"
            except:
                pass

        header = QHBoxLayout()
        info = QLabel(f"<b>{self.patient['nom']}</b><br/>{age_str}")
        info.setStyleSheet("font-size: 14px;")
        
        btn_consult = QPushButton("➕ Nouvelle Consultation")
        btn_consult.clicked.connect(self.accept_consult)
        
        header.addWidget(info)
        header.addStretch()
        header.addWidget(btn_consult)
        layout.addLayout(header)

        layout.addWidget(QLabel("<b>Historique des consultations :</b>"))
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Date", "Motif"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.itemDoubleClicked.connect(self.view_pdf)
        layout.addWidget(self.table)
        
        self.load_history()

    def load_history(self):
        consults = get_consultations(self.patient['id'])
        self.table.setRowCount(0)
        for c in consults:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(c[1])))
            self.table.setItem(row, 1, QTableWidgetItem(str(c[2])))

    def accept_consult(self):
        self.resultat = "consult"
        self.accept()

    def view_pdf(self, item):
        date_str = self.table.item(item.row(), 0).text()
        
        # FORMAT SYNCHRONISÉ AVEC CONSULTATION_FORM
        pdf_path = f"exports/consult_{self.patient['id']}_{date_str}.pdf"
        
        if os.path.exists(pdf_path):
            os.startfile(os.path.abspath(pdf_path))
        else:
            QMessageBox.warning(self, "Erreur", f"Fichier PDF introuvable :\n{pdf_path}")