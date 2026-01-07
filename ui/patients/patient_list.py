from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QLineEdit, QLabel
)

from services.patient_service import get_patients, delete_patient
from ui.patients.patient_form import PatientForm
from ui.patients.patient_profile import PatientProfile


class PatientList(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Patients")
        self.resize(900, 500)

        self.all_patients = []  # cache pour la recherche

        self.setup_ui()
        self.load_data()

    # ======================================================
    # UI
    # ======================================================
    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # ---------- BARRE D'ACTIONS ----------
        actions_layout = QHBoxLayout()

        self.add_btn = QPushButton("➕ Ajouter")
        self.edit_btn = QPushButton("✏️ Modifier")
        self.view_btn = QPushButton("👁️ Consulter profil")
        self.del_btn = QPushButton("🗑️ Supprimer")

        self.add_btn.clicked.connect(self.add_patient)
        self.edit_btn.clicked.connect(self.edit_patient)
        self.view_btn.clicked.connect(self.open_profile)
        self.del_btn.clicked.connect(self.delete_patient)

        for b in [self.add_btn, self.edit_btn, self.view_btn, self.del_btn]:
            actions_layout.addWidget(b)

        main_layout.addLayout(actions_layout)

        # ---------- BARRE DE RECHERCHE ----------
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍 Rechercher :")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Nom, téléphone ou assurance..."
        )
        self.search_input.textChanged.connect(self.apply_filter)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)

        main_layout.addLayout(search_layout)

        # ---------- TABLE ----------
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nom", "Téléphone", "Assurance", "1ère consultation"
        ])
        self.table.cellDoubleClicked.connect(self.open_profile)

        main_layout.addWidget(self.table)

    # ======================================================
    # DATA
    # ======================================================
    def load_data(self):
        self.all_patients = get_patients()
        self.display_patients(self.all_patients)

    def display_patients(self, patients):
        self.table.setRowCount(0)

        for p in patients:
            row = self.table.rowCount()
            self.table.insertRow(row)

            for col, value in enumerate(p):
                self.table.setItem(
                    row, col, QTableWidgetItem(str(value))
                )

    # ======================================================
    # SEARCH
    # ======================================================
    def apply_filter(self, text):
        text = text.lower().strip()

        if not text:
            self.display_patients(self.all_patients)
            return

        filtered = []
        for p in self.all_patients:
            # p = (id, nom, téléphone, assurance, date)
            if (
                text in str(p[1]).lower()
                or text in str(p[2]).lower()
                or text in str(p[3]).lower()
            ):
                filtered.append(p)

        self.display_patients(filtered)

    # ======================================================
    # UTILS
    # ======================================================
    def get_selected_patient(self):
        row = self.table.currentRow()
        if row < 0:
            return None

        return {
            "id": int(self.table.item(row, 0).text()),
            "nom": self.table.item(row, 1).text(),
            "telephone": self.table.item(row, 2).text(),
            "assurance": self.table.item(row, 3).text()
        }

    # ======================================================
    # ACTIONS
    # ======================================================
    def add_patient(self):
        self.form = PatientForm(self.load_data)
        self.form.show()

    def edit_patient(self):
        patient = self.get_selected_patient()
        if not patient:
            QMessageBox.warning(
                self, "Erreur", "Sélectionnez un patient"
            )
            return

        self.form = PatientForm(self.load_data, patient)
        self.form.show()

    def open_profile(self):
        patient = self.get_selected_patient()
        if not patient:
            QMessageBox.warning(
                self, "Erreur", "Sélectionnez un patient"
            )
            return

        self.profile = PatientProfile(patient)
        self.profile.show()

    def delete_patient(self):
        patient = self.get_selected_patient()
        if not patient:
            QMessageBox.warning(
                self, "Erreur", "Sélectionnez un patient"
            )
            return

        confirm = QMessageBox.question(
            self,
            "Confirmation",
            f"Supprimer le patient {patient['nom']} ?"
        )

        if confirm == QMessageBox.StandardButton.Yes:
            delete_patient(patient["id"])
            self.load_data()
