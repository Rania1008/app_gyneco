from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel,
    QHBoxLayout, QVBoxLayout, QStackedWidget,
    QCalendarWidget, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QTextCharFormat, QColor

from ui.widgets.sidebar import Sidebar
from ui.patients.patient_list import PatientList
from ui.rendezvous.rdv_list import RDVList
from services.rendezvous_service import (
    get_rdv_dates, get_rdv_by_date
)


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
        main_layout = QHBoxLayout()

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
            "font-size:18px; font-weight:bold; padding:10px;"
        )
        home_layout.addWidget(title)

        # --- CALENDRIER ---
        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.on_date_selected)
        home_layout.addWidget(self.calendar)

        # --- TABLE RDV ---
        self.rdv_table = QTableWidget(0, 3)
        self.rdv_table.setHorizontalHeaderLabels(
            ["Heure", "Patiente", "Statut"]
        )
        self.rdv_table.horizontalHeader().setStretchLastSection(True)
        home_layout.addWidget(self.rdv_table)

        self.page_home.setLayout(home_layout)

        # ---------- AUTRES PAGES ----------
        self.page_patients = PatientList()
        self.page_rdv = RDVList()

        self.stack.addWidget(self.page_home)
        self.stack.addWidget(self.page_patients)
        self.stack.addWidget(self.page_rdv)

        main_layout.addWidget(self.stack)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # ===== MENU =====
        self.sidebar.btn_dashboard.clicked.connect(self.show_home)
        self.sidebar.btn_patients.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_patients)
        )
        self.sidebar.btn_rdv.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.page_rdv)
        )
        self.sidebar.btn_salle.clicked.connect(self.not_implemented)
        self.sidebar.btn_facture.clicked.connect(self.not_implemented)

        # ===== INIT =====
        self.highlight_rdv_days()
        self.on_date_selected(QDate.currentDate())

    # =========================
    # CALENDRIER
    # =========================
    def highlight_rdv_days(self):
        self.calendar.setDateTextFormat(QDate(), QTextCharFormat())
        fmt = QTextCharFormat()
        fmt.setBackground(QColor("#AED6F1"))

        for d in get_rdv_dates():
            qdate = QDate.fromString(d, "yyyy-MM-dd")
            if qdate.isValid():
                self.calendar.setDateTextFormat(qdate, fmt)

    def on_date_selected(self, qdate):
        date_str = qdate.toString("yyyy-MM-dd")
        rdvs = get_rdv_by_date(date_str)

        self.rdv_table.setRowCount(0)

        if not rdvs:
            self.rdv_table.setRowCount(1)
            self.rdv_table.setItem(0, 0, QTableWidgetItem("—"))
            self.rdv_table.setItem(
                0, 1, QTableWidgetItem("Aucun rendez-vous")
            )
            self.rdv_table.setItem(0, 2, QTableWidgetItem("—"))
            return

        for r in rdvs:
            row = self.rdv_table.rowCount()
            self.rdv_table.insertRow(row)
            for c, v in enumerate(r):
                self.rdv_table.setItem(
                    row, c, QTableWidgetItem(str(v))
                )

    def show_home(self):
        self.highlight_rdv_days()
        self.on_date_selected(self.calendar.selectedDate())
        self.stack.setCurrentWidget(self.page_home)

    def not_implemented(self):
        temp = QLabel("Module en cours de développement 🚧")
        temp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        temp.setStyleSheet("font-size:16px;")
        self.stack.addWidget(temp)
        self.stack.setCurrentWidget(temp)
