from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QTextEdit,
    QPushButton, QMessageBox
)
from services.consultation_service import add_consultation, update_consultation

class ConsultationForm(QWidget):

    def __init__(self, patient_id, refresh_callback, consultation=None):
        super().__init__()
        self.patient_id = patient_id
        self.consultation = consultation
        self.refresh_callback = refresh_callback
        self.setWindowTitle("Consultation")
        self.resize(600, 600)
        self.setup_ui()
        if consultation:
            self.fill_form()

    def setup_ui(self):
        layout = QFormLayout()

        self.antecedants = QTextEdit()
        self.motif = QTextEdit()
        self.examen_clinique = QTextEdit()
        self.examen_biologique = QTextEdit()
        self.examen_radiologique = QTextEdit()
        self.diagnostique = QTextEdit()
        self.traitement = QTextEdit()

        save_btn = QPushButton("Enregistrer")
        save_btn.clicked.connect(self.save)

        layout.addRow("Antécédents", self.antecedants)
        layout.addRow("Motif *", self.motif)
        layout.addRow("Examen clinique *", self.examen_clinique)
        layout.addRow("Examen biologique", self.examen_biologique)
        layout.addRow("Examen radiologique", self.examen_radiologique)
        layout.addRow("Diagnostique *", self.diagnostique)
        layout.addRow("Traitement *", self.traitement)
        layout.addRow(save_btn)

        self.setLayout(layout)

    def fill_form(self):
        self.antecedants.setPlainText(self.consultation[2])
        self.motif.setPlainText(self.consultation[3])
        self.examen_clinique.setPlainText(self.consultation[4])
        self.examen_biologique.setPlainText(self.consultation[5])
        self.examen_radiologique.setPlainText(self.consultation[6])
        self.diagnostique.setPlainText(self.consultation[7])
        self.traitement.setPlainText(self.consultation[8])

    def save(self):
        if not self.motif.toPlainText().strip() \
           or not self.examen_clinique.toPlainText().strip() \
           or not self.diagnostique.toPlainText().strip() \
           or not self.traitement.toPlainText().strip():
            QMessageBox.warning(self, "Erreur", "Champs obligatoires manquants")
            return

        data = {
            "antecedants": self.antecedants.toPlainText(),
            "motif_consultation": self.motif.toPlainText(),
            "examen_clinique": self.examen_clinique.toPlainText(),
            "examen_biologique": self.examen_biologique.toPlainText(),
            "examen_radiologique": self.examen_radiologique.toPlainText(),
            "diagnostique": self.diagnostique.toPlainText(),
            "traitement": self.traitement.toPlainText()
        }

        if self.consultation:
            update_consultation(self.consultation[0], data)
        else:
            data["patient_id"] = self.patient_id
            add_consultation(data)

        self.refresh_callback()
        self.close()
