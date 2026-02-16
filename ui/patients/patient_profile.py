from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QMessageBox
from services.consultation_service import get_consultations
from services.patient_service import get_patient_by_id

class PatientProfile(QWidget):
    def __init__(self, patient_id, conn):
        super().__init__()
        self.patient_id = patient_id
        self.conn = conn
        self.setWindowTitle("Profil Patiente")
        self.resize(700, 500)
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Infos patiente
        self.info_label = QLabel("Chargement...")
        self.info_label.setStyleSheet("background: #f0f0f0; padding: 10px; border-radius: 5px;")
        layout.addWidget(self.info_label)

        layout.addWidget(QLabel("<b>Historique des consultations :</b>"))
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["ID", "Date"])
        layout.addWidget(self.table)

        self.empty_msg = QLabel("Aucune consultation enregistrée.")
        self.empty_msg.setStyleSheet("color: gray; font-style: italic;")
        self.empty_msg.hide()
        layout.addWidget(self.empty_msg)

    def load_data(self):
        # 1. Charger infos patiente
        p = get_patient_by_id(self.patient_id)
        if p:
            self.info_label.setText(f"Nom : {p['nom']}\nTel : {p['telephone']}\nAssurance : {p['assurance']}")

        # 2. Charger consultations
        consults = get_consultations(self.patient_id)
        self.table.setRowCount(0)
        
        if not consults:
            self.empty_msg.show()
            self.table.hide()
        else:
            self.empty_msg.hide()
            self.table.show()
            for c in consults:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(c[0])))
                self.table.setItem(row, 1, QTableWidgetItem(str(c[1])))