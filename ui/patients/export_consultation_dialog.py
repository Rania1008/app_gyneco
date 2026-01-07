from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QCheckBox,
    QPushButton, QFileDialog
)
from utils.pdf_consultation import export_consultation_pdf

class ExportConsultationDialog(QDialog):

    def __init__(self, patient_name, consultation):
        super().__init__()
        self.patient_name = patient_name
        self.consultation = consultation
        self.setWindowTitle("Exporter la consultation")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.fields = {
            "Antécédents": ("antecedants", QCheckBox("Antécédents")),
            "Motif": ("motif", QCheckBox("Motif")),
            "Examen clinique": ("examen_clinique", QCheckBox("Examen clinique")),
            "Examen biologique": ("examen_biologique", QCheckBox("Examen biologique")),
            "Examen radiologique": ("examen_radiologique", QCheckBox("Examen radiologique")),
            "Diagnostique": ("diagnostique", QCheckBox("Diagnostique")),
            "Traitement": ("traitement", QCheckBox("Traitement"))
        }

        for _, (_, chk) in self.fields.items():
            chk.setChecked(True)
            layout.addWidget(chk)

        export_btn = QPushButton("Exporter en PDF")
        export_btn.clicked.connect(self.export)
        layout.addWidget(export_btn)

        self.setLayout(layout)

    def export(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer le PDF", "consultation.pdf", "PDF (*.pdf)"
        )
        if not path:
            return

        sections = {}
        for title, (key, chk) in self.fields.items():
            if chk.isChecked():
                sections[title] = self.consultation.get(key, "")

        export_consultation_pdf(
            path,
            self.patient_name,
            self.consultation["date"],
            sections
        )

        self.accept()
