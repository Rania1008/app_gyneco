from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QTextEdit,
    QDateEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import QDate
from services.suivi_service import add_suivi


class SuiviForm(QWidget):

    def __init__(self, patient_id, refresh_callback):
        super().__init__()
        self.patient_id = patient_id
        self.refresh_callback = refresh_callback
        self.setWindowTitle("Ajouter un suivi patient")
        self.resize(500, 450)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout()

        self.date_suivi = QDateEdit()
        self.date_suivi.setCalendarPopup(True)
        self.date_suivi.setDate(QDate.currentDate())

        self.evolution_clinique = QTextEdit()
        self.examen_biologique = QTextEdit()
        self.examen_radiologique = QTextEdit()
        self.traitement = QTextEdit()

        save_btn = QPushButton("Enregistrer")
        save_btn.clicked.connect(self.save)

        layout.addRow("Date du suivi *", self.date_suivi)
        layout.addRow("Évolution clinique *", self.evolution_clinique)
        layout.addRow("Examen biologique", self.examen_biologique)
        layout.addRow("Examen radiologique", self.examen_radiologique)
        layout.addRow("Traitement", self.traitement)
        layout.addRow(save_btn)

        self.setLayout(layout)

    def save(self):
        if not self.evolution_clinique.toPlainText().strip():
            QMessageBox.warning(
                self,
                "Erreur",
                "L’évolution clinique est obligatoire"
            )
            return

        add_suivi({
            "patient_id": self.patient_id,
            "date_suivi": self.date_suivi.date().toString("yyyy-MM-dd"),
            "evolution_clinique": self.evolution_clinique.toPlainText(),
            "examen_biologique": self.examen_biologique.toPlainText(),
            "examen_radiologique": self.examen_radiologique.toPlainText(),
            "traitement": self.traitement.toPlainText()
        })

        self.refresh_callback()
        self.close()
