from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QTextEdit,
    QDateEdit, QComboBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import QDate
from services.grossesse_service import add_grossesse


class GrossesseForm(QWidget):

    def __init__(self, patient_id, refresh_callback):
        super().__init__()
        self.patient_id = patient_id
        self.refresh_callback = refresh_callback
        self.setWindowTitle("Ajouter une grossesse")
        self.resize(500, 500)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout()

        self.date_derniere_regle = QDateEdit()
        self.date_derniere_regle.setCalendarPopup(True)
        self.date_derniere_regle.setDate(QDate.currentDate())

        self.grossesse_precedente = QTextEdit()
        self.fetus = QTextEdit()

        self.status = QComboBox()
        self.status.addItems(["En cours", "À terme", "Interrompue"])

        self.a_terme_le = QDateEdit()
        self.a_terme_le.setCalendarPopup(True)
        self.a_terme_le.setDate(QDate.currentDate())

        self.notes = QTextEdit()

        save_btn = QPushButton("Enregistrer")
        save_btn.clicked.connect(self.save)

        layout.addRow("Date dernière règle *", self.date_derniere_regle)
        layout.addRow("Grossesse précédente", self.grossesse_precedente)
        layout.addRow("Fœtus", self.fetus)
        layout.addRow("Statut", self.status)
        layout.addRow("À terme le", self.a_terme_le)
        layout.addRow("Notes", self.notes)
        layout.addRow(save_btn)

        self.setLayout(layout)

    def save(self):
        add_grossesse({
            "patient_id": self.patient_id,
            "date_derniere_regle": self.date_derniere_regle.date().toString("yyyy-MM-dd"),
            "grossesse_precedente": self.grossesse_precedente.toPlainText(),
            "fetus": self.fetus.toPlainText(),
            "status": self.status.currentText(),
            "a_terme_le": self.a_terme_le.date().toString("yyyy-MM-dd"),
            "notes": self.notes.toPlainText()
        })

        self.refresh_callback()
        self.close()
