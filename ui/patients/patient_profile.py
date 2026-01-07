from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QTabWidget, QTableWidget, QTableWidgetItem, QMessageBox
)

from services.consultation_service import get_consultations
from services.suivi_service import get_suivis
from services.grossesse_service import get_grossesses

from ui.patients.consultation_form import ConsultationForm
from ui.patients.suivi_form import SuiviForm
from ui.patients.grossesse_form import GrossesseForm


class PatientProfile(QWidget):

    def __init__(self, patient: dict):
        super().__init__()
        self.patient = patient
        self.setWindowTitle(f"Profil patient - {patient['nom']}")
        self.resize(900, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.info = QLabel(
            f"<b>Nom :</b> {patient['nom']}<br>"
            f"<b>Téléphone :</b> {patient.get('telephone','')}<br>"
            f"<b>Assurance :</b> {patient.get('assurance','')}"
        )
        self.layout.addWidget(self.info)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.init_consultations_tab()
        self.init_suivi_tab()
        self.init_grossesse_tab()

        self.load_all()

    # ---------------- CONSULTATIONS ----------------
    def init_consultations_tab(self):
        self.consult_tab = QWidget()
        layout = QVBoxLayout(self.consult_tab)

        btn = QPushButton("➕ Ajouter consultation")
        btn.clicked.connect(self.add_consultation)
        layout.addWidget(btn)

        self.consult_table = QTableWidget(0, 9)
        self.consult_table.setHorizontalHeaderLabels([
            "ID", "Date", "Antécédents", "Motif",
            "Clinique", "Biologique", "Radiologique",
            "Diagnostique", "Traitement"
        ])
        layout.addWidget(self.consult_table)

        self.tabs.addTab(self.consult_tab, "Consultations")

    # ---------------- SUIVI ----------------
    def init_suivi_tab(self):
        self.suivi_tab = QWidget()
        layout = QVBoxLayout(self.suivi_tab)

        btn = QPushButton("➕ Ajouter suivi")
        btn.clicked.connect(self.add_suivi)
        layout.addWidget(btn)

        self.suivi_table = QTableWidget(0, 6)
        self.suivi_table.setHorizontalHeaderLabels([
            "ID", "Date", "Évolution",
            "Biologique", "Radiologique", "Traitement"
        ])
        layout.addWidget(self.suivi_table)

        self.tabs.addTab(self.suivi_tab, "Suivi patient")

    # ---------------- GROSSESSE ----------------
    def init_grossesse_tab(self):
        self.gross_tab = QWidget()
        layout = QVBoxLayout(self.gross_tab)

        btn = QPushButton("➕ Ajouter grossesse")
        btn.clicked.connect(self.add_grossesse)
        layout.addWidget(btn)

        self.gross_table = QTableWidget(0, 7)
        self.gross_table.setHorizontalHeaderLabels([
            "ID", "DDR", "Grossesse préc.",
            "Fœtus", "Statut", "Terme", "Notes"
        ])
        layout.addWidget(self.gross_table)

        self.tabs.addTab(self.gross_tab, "Grossesse")

    # ---------------- LOAD ----------------
    def load_all(self):
        self.load_consultations()
        self.load_suivi()
        self.load_grossesse()

    def load_consultations(self):
        self.consult_table.setRowCount(0)
        for row in get_consultations(self.patient["id"]):
            r = self.consult_table.rowCount()
            self.consult_table.insertRow(r)
            for c, v in enumerate(row):
                self.consult_table.setItem(r, c, QTableWidgetItem(str(v)))

    def load_suivi(self):
        self.suivi_table.setRowCount(0)
        for row in get_suivis(self.patient["id"]):
            r = self.suivi_table.rowCount()
            self.suivi_table.insertRow(r)
            for c, v in enumerate(row):
                self.suivi_table.setItem(r, c, QTableWidgetItem(str(v)))

    def load_grossesse(self):
        self.gross_table.setRowCount(0)
        for row in get_grossesses(self.patient["id"]):
            r = self.gross_table.rowCount()
            self.gross_table.insertRow(r)
            for c, v in enumerate(row):
                self.gross_table.setItem(r, c, QTableWidgetItem(str(v)))

    # ---------------- ACTIONS ----------------
    def add_consultation(self):
        self.f = ConsultationForm(self.patient["id"], self.load_consultations)
        self.f.show()

    def add_suivi(self):
        self.f = SuiviForm(self.patient["id"], self.load_suivi)
        self.f.show()

    def add_grossesse(self):
        self.f = GrossesseForm(self.patient["id"], self.load_grossesse)
        self.f.show()
