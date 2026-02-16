from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QLineEdit, QLabel
)
from PyQt6.QtCore import Qt

# Imports des services et composants
from services.patient_service import get_patients, delete_patient, get_patient_by_id
from ui.patients.patient_form import PatientForm
from ui.patients.patient_profile import PatientProfile
from ui.patients.action_selector import ActionSelector
from ui.patients.consultation_form import ConsultationForm
from config.database import get_connection

class PatientList(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Patients")
        self.resize(900, 500)

        self.conn = get_connection()
        self.all_patients = []
        
        # Références pour éviter que les fenêtres ne soient fermées par le Garbage Collector
        self.form_window = None
        self.profile_window = None
        self.consult_window = None

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Barre d'actions supérieure
        actions = QHBoxLayout()
        self.add_btn = QPushButton("➕ Ajouter")
        self.edit_btn = QPushButton("✏️ Modifier")
        self.view_btn = QPushButton("👁️ Consulter / Action")
        self.del_btn = QPushButton("🗑️ Supprimer")

        # Connexion des signaux
        self.add_btn.clicked.connect(self.add_patient)
        self.edit_btn.clicked.connect(self.edit_patient)
        self.view_btn.clicked.connect(self.open_action_selector)
        self.del_btn.clicked.connect(self.delete_patient)

        for b in [self.add_btn, self.edit_btn, self.view_btn, self.del_btn]:
            actions.addWidget(b)

        layout.addLayout(actions)

        # Barre de recherche
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher par nom, téléphone ou ID...")
        self.search_input.textChanged.connect(self.apply_filter)
        search_layout.addWidget(QLabel("🔍"))
        search_layout.addWidget(self.search_input)

        layout.addLayout(search_layout)

        # Tableau des patients
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Nom", "Téléphone", "Assurance", "1ère consultation"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

    def load_data(self):
        """Recharge les données depuis la base de données"""
        self.all_patients = get_patients()
        self.display(self.all_patients)

    def display(self, patients):
        """Affiche la liste filtrée dans le tableau"""
        self.table.setRowCount(0)
        for p in patients:
            row = self.table.rowCount()
            self.table.insertRow(row)
            # On assume que p est un tuple/liste venant de la DB (ID, Nom, Tel, etc.)
            for i in range(5):
                val = p[i] if i < len(p) else ""
                item = QTableWidgetItem(str(val))
                self.table.setItem(row, i, item)

    def apply_filter(self, text):
        """Filtre dynamique lors de la saisie"""
        search_text = text.lower()
        filtered = [
            p for p in self.all_patients
            if any(search_text in str(field).lower() for field in p)
        ]
        self.display(filtered)

    def get_selected_patient_id(self):
        """Récupère l'ID de la ligne sélectionnée"""
        row = self.table.currentRow()
        if row < 0:
            return None
        return int(self.table.item(row, 0).text())

    def add_patient(self):
        """Ouvre le formulaire pour un nouveau patient"""
        self.form_window = PatientForm(self.load_data)
        self.form_window.show()

    def edit_patient(self):
        """Récupère les données complètes et ouvre le formulaire en mode édition"""
        pid = self.get_selected_patient_id()
        if not pid:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner une patiente à modifier.")
            return
        
        # Correction du crash : on récupère le dictionnaire complet
        patient_data = get_patient_by_id(pid)
        if patient_data:
            self.form_window = PatientForm(self.load_data, patient_data)
            self.form_window.show()

    def open_action_selector(self):
        """Ouvre la boîte de dialogue pour choisir entre Profil ou Nouvelle Consultation"""
        pid = self.get_selected_patient_id()
        if not pid:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner une patiente.")
            return
        
        # CORRECTION ICI : On récupère le dictionnaire complet, pas juste le nom
        patient_data = get_patient_by_id(pid) 
        
        if patient_data:
            # On passe tout le dictionnaire à ActionSelector
            selector = ActionSelector(patient_data) 
            if selector.exec():
                if selector.resultat == "consult":
                    # On passe aussi le dictionnaire au formulaire de consultation
                    self.consult_window = ConsultationForm(patient_data, self.load_data)
                    self.consult_window.show()
                elif selector.resultat == "profile":
                    self.profile_window = PatientProfile(pid, self.conn)
                    self.profile_window.show()

    def delete_patient(self):
        """Supprime la patiente après confirmation"""
        pid = self.get_selected_patient_id()
        if not pid:
            return
        
        reply = QMessageBox.question(
            self, "Confirmation", 
            "Êtes-vous sûr de vouloir supprimer cette patiente ? Cela supprimera également son historique.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            delete_patient(pid)
            self.load_data()