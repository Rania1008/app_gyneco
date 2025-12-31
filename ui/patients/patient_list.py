from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem
)
from services.patient_service import get_patients
from ui.patients.patient_form import PatientForm

class PatientList(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout()

        add_btn = QPushButton("➕ Nouveau patient")
        add_btn.clicked.connect(self.open_form)
        layout.addWidget(add_btn)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nom", "Téléphone", "Assurance", "1ère consultation"
        ])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_data(self):
        self.table.setRowCount(0)
        for row_data in get_patients():
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, value in enumerate(row_data):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def open_form(self):
        self.form = PatientForm(refresh_callback=self.load_data)
        self.form.show()
