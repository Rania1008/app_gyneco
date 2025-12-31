from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout

class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.btn_dashboard = QPushButton("🏠 Accueil")
        self.btn_patients = QPushButton("🧍‍♀️ Patients")
        self.btn_salle = QPushButton("🪑 Salle d’attente")
        self.btn_rdv = QPushButton("📅 Rendez-vous")
        self.btn_consult = QPushButton("🩺 Consultations")
        self.btn_facture = QPushButton("🧾 Facturation")

        for btn in [
            self.btn_dashboard,
            self.btn_patients,
            self.btn_salle,
            self.btn_rdv,
            self.btn_consult,
            self.btn_facture
        ]:
            btn.setFixedHeight(40)
            layout.addWidget(btn)

        layout.addStretch()
        self.setLayout(layout)
