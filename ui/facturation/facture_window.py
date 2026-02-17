import os
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QFormLayout, QLineEdit, QComboBox, 
                             QPushButton, QVBoxLayout, QMessageBox, QTextEdit)
from models.facture_model import FactureModel
from services.facture_service import save_facture
from utils.pdf_facture import generer_ticket_caisse

class FactureWindow(QWidget):
    def __init__(self, refresh_callback):
        super().__init__()
        self.refresh_callback = refresh_callback
        self.setWindowTitle("Nouvelle Facture - Secrétariat")
        self.resize(450, 500)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.combo_patient = QComboBox()
        for p_id, p_nom in FactureModel.get_list_patients():
            self.combo_patient.addItem(p_nom, p_id)

        self.actes_libres = QTextEdit()
        self.actes_libres.setPlaceholderText("Saisissez les actes effectués...")
        self.actes_libres.setFixedHeight(80)

        self.total = QLineEdit()
        self.paye = QLineEdit("0")
        
        self.reste = QLineEdit("0.00")
        self.reste.setReadOnly(True)
        # Correction : color: black pour éviter l'affichage blanc invisible
        self.reste.setStyleSheet("background-color: white; color: black; font-weight: bold; padding: 5px;")

        self.total.textChanged.connect(self.calculer_reste)
        self.paye.textChanged.connect(self.calculer_reste)

        form.addRow("Patiente :", self.combo_patient)
        form.addRow("Détail Actes :", self.actes_libres)
        form.addRow("Total (DH) :", self.total)
        form.addRow("Versé (DH) :", self.paye)
        form.addRow("Reste à Payer :", self.reste)

        btn_save = QPushButton("💾 Enregistrer et Imprimer Ticket")
        btn_save.setStyleSheet("background-color: #27ae60; color: white; height: 45px; font-weight: bold;")
        btn_save.clicked.connect(self.valider)

        layout.addLayout(form)
        layout.addWidget(btn_save)

    def calculer_reste(self):
        try:
            t = float(self.total.text() or 0)
            p = float(self.paye.text() or 0)
            self.reste.setText(f"{t - p:.2f}")
        except: pass

    def valider(self):
        if not self.total.text().strip():
            QMessageBox.warning(self, "Erreur", "Le montant est obligatoire.")
            return

        p_id = self.combo_patient.currentData()
        p_nom = self.combo_patient.currentText()
        ref = f"FAC-{datetime.now().strftime('%y%m%d-%H%M%S')}"
        
        data = {
            "patient_id": p_id, "total": float(self.total.text()),
            "paye": float(self.paye.text()), "reference": ref,
            "notes": self.actes_libres.toPlainText()
        }

        try:
            save_facture(data)
            if not os.path.exists("exports/factures"): os.makedirs("exports/factures")
            pdf_path = f"exports/factures/ticket_{ref}.pdf"
            generer_ticket_caisse(pdf_path, p_nom, ref, data["notes"], data["total"], data["paye"], self.reste.text())
            os.startfile(os.path.abspath(pdf_path))
            QMessageBox.information(self, "Succès", "Facture enregistrée.")
            self.refresh_callback()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))