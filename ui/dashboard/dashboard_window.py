from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel,
    QHBoxLayout, QVBoxLayout, QStackedWidget
)
from PyQt6.QtCore import Qt

from ui.widgets.sidebar import Sidebar
from ui.patients.patient_list import PatientList
from ui.rendezvous.rdv_list import RDVList


class DashboardWindow(QMainWindow):

    def __init__(self, user):
        super().__init__()
        self.user = user

        self.setWindowTitle("Cabinet de gynécologie – Gestion")
        self.resize(1200, 700)

        self.setup_ui()

    def setup_ui(self):
        # ===== CENTRAL =====
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        # ===== SIDEBAR =====
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # ===== STACK =====
        self.stack = QStackedWidget()

        # ---------- PAGE ACCUEIL ----------
        self.page_home = QWidget()
        home_layout = QVBoxLayout()

        title = QLabel(f"Bienvenue {self.user['username']} 👋")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "font-size:18px; font-weight:bold; padding:15px;"
        )

        subtitle = QLabel(
            "Système de gestion d’un cabinet de gynécologie"
        )
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color:gray;")

        home_layout.addWidget(title)
        home_layout.addWidget(subtitle)
        self.page_home.setLayout(home_layout)

        # ---------- ONGLET PATIENTS ----------
        self.page_patients = PatientList()

        # ---------- ONGLET CONSULTATIONS ----------
        # RDVList = ton onglet consultations (liste + ajout)
        self.page_consultations = RDVList()

        # ---------- AJOUT AU STACK ----------
        self.stack.addWidget(self.page_home)
        self.stack.addWidget(self.page_patients)
        self.stack.addWidget(self.page_consultations)

        main_layout.addWidget(self.stack)
        self.setCentralWidget(central_widget)

        # ===== MENU =====
        self.sidebar.btn_dashboard.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_home)
        )

        self.sidebar.btn_patients.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_patients)
        )

        self.sidebar.btn_rdv.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_consultations)
        )

        # Salle d’attente (non implémentée pour l’instant)
        self.sidebar.btn_salle.clicked.connect(self.not_implemented)

        # Facturation PAS indépendante (depuis consultation)
        self.sidebar.btn_facture.clicked.connect(self.facture_info)

    # =========================
    # INFOS
    # =========================
    def not_implemented(self):
        page = QLabel("Module en cours de développement 🚧")
        page.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)

    def facture_info(self):
        page = QLabel(
            "La facturation se fait depuis une consultation existante."
        )
        page.setAlignment(Qt.AlignmentFlag.AlignCenter)
        page.setStyleSheet("font-size:15px;")
        self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)
