from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel,
    QHBoxLayout, QVBoxLayout, QStackedWidget
)
from PyQt6.QtCore import Qt

from ui.widgets.sidebar import Sidebar
from ui.patients.patient_list import PatientList


class DashboardWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Cabinet de gynécologie – Gestion")
        self.resize(1200, 700)
        self.setup_ui()

    def setup_ui(self):
        # Widget central
        central_widget = QWidget()
        main_layout = QHBoxLayout()

        # ===== SIDEBAR =====
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # ===== ZONE CENTRALE (STACK) =====
        self.stack = QStackedWidget()

        # --- PAGE ACCUEIL ---
        self.page_home = QWidget()
        home_layout = QVBoxLayout()

        welcome_label = QLabel(
            f"Bienvenue {self.user['username']} 👋\n\n"
            "Logiciel de gestion du cabinet de gynécologie"
        )
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet(
            "font-size:18px; font-weight:bold; padding:40px;"
        )

        home_layout.addWidget(welcome_label)
        self.page_home.setLayout(home_layout)

        # --- PAGE PATIENTS ---
        self.page_patients = PatientList()

        # Ajouter les pages au stack
        self.stack.addWidget(self.page_home)
        self.stack.addWidget(self.page_patients)

        main_layout.addWidget(self.stack)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # ===== CONNEXIONS MENU =====
        self.sidebar.btn_dashboard.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_home)
        )

        self.sidebar.btn_patients.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_patients)
        )

        # (préparé pour plus tard)
        self.sidebar.btn_salle.clicked.connect(self.not_implemented)
        self.sidebar.btn_rdv.clicked.connect(self.not_implemented)
        self.sidebar.btn_facture.clicked.connect(self.not_implemented)

    def not_implemented(self):
        """Page temporaire pour les modules non encore codés"""
        temp = QLabel("Module en cours de développement 🚧")
        temp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        temp.setStyleSheet("font-size:16px;")
        self.stack.addWidget(temp)
        self.stack.setCurrentWidget(temp)
