from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt

from services.facture_service import FactureService


class FactureWindow(QWidget):

    def __init__(self, patient_id, consultation_id, conn):
        super().__init__()

        self.patient_id = patient_id
        self.consultation_id = consultation_id
        self.conn = conn
        self.actes = []

        self.setWindowTitle("Facturation")
        self.resize(600, 400)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🧾 Création de facture")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(title)

        # === AJOUT ACTE ===
        acte_layout = QHBoxLayout()

        self.service_input = QLineEdit()
        self.service_input.setPlaceholderText("Acte médical")

        self.frais_input = QLineEdit()
        self.frais_input.setPlaceholderText("Frais")

        btn_add = QPushButton("Ajouter")
        btn_add.clicked.connect(self.ajouter_acte)

        acte_layout.addWidget(self.service_input)
        acte_layout.addWidget(self.frais_input)
        acte_layout.addWidget(btn_add)

        layout.addLayout(acte_layout)

        # === TABLE ACTES ===
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Acte", "Frais"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        # === MONTANTS ===
        montant_layout = QHBoxLayout()

        self.label_total = QLabel("Total : 0")
        self.input_paye = QLineEdit()
        self.input_paye.setPlaceholderText("Montant payé")
        self.input_paye.textChanged.connect(self.update_reste)

        self.label_reste = QLabel("Reste : 0")

        montant_layout.addWidget(self.label_total)
        montant_layout.addWidget(self.input_paye)
        montant_layout.addWidget(self.label_reste)

        layout.addLayout(montant_layout)

        # === VALIDER ===
        btn_valider = QPushButton("Créer la facture")
        btn_valider.clicked.connect(self.creer_facture)
        layout.addWidget(btn_valider)

        self.setLayout(layout)

    # ================= LOGIQUE =================

    def ajouter_acte(self):
        service = self.service_input.text().strip()

        try:
            frais = float(self.frais_input.text())
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Frais invalides")
            return

        if not service:
            QMessageBox.warning(self, "Erreur", "Acte obligatoire")
            return

        self.actes.append({"service": service, "frais": frais})

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(service))
        self.table.setItem(row, 1, QTableWidgetItem(str(frais)))

        self.service_input.clear()
        self.frais_input.clear()

        self.update_total()

    def update_total(self):
        total = FactureService.calculer_total(self.actes)
        self.label_total.setText(f"Total : {total}")
        self.update_reste()

    def update_reste(self):
        try:
            paye = float(self.input_paye.text())
        except ValueError:
            paye = 0

        total = FactureService.calculer_total(self.actes)
        reste = total - paye
        self.label_reste.setText(f"Reste : {reste}")

    def creer_facture(self):
        try:
            paye = float(self.input_paye.text())
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Montant payé invalide")
            return

        try:
            FactureService.creer_facture(
                self.patient_id,
                self.consultation_id,
                self.actes,
                paye,
                self.conn
            )
            QMessageBox.information(self, "Succès", "Facture créée avec succès")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))
