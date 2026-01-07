from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from services.rendezvous_service import (
    get_rendezvous, delete_rdv
)
from ui.rendezvous.rdv_form import RDVForm


class RDVList(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rendez-vous")
        self.resize(700, 400)
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("➕ Ajouter")
        self.edit_btn = QPushButton("✏️ Modifier")
        self.del_btn = QPushButton("🗑️ Supprimer")

        self.add_btn.clicked.connect(self.add_rdv)
        self.edit_btn.clicked.connect(self.edit_rdv)
        self.del_btn.clicked.connect(self.delete_rdv)

        for b in [self.add_btn, self.edit_btn, self.del_btn]:
            btn_layout.addWidget(b)

        layout.addLayout(btn_layout)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Patiente", "Date", "Heure", "Statut"
        ])
        layout.addWidget(self.table)

    def load_data(self):
        self.table.setRowCount(0)
        self.data = get_rendezvous()

        for r in self.data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for c, v in enumerate(r):
                self.table.setItem(
                    row, c, QTableWidgetItem(str(v))
                )

    def get_selected(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        return self.data[row]

    def add_rdv(self):
        self.form = RDVForm(self.load_data)
        self.form.show()

    def edit_rdv(self):
        rdv = self.get_selected()
        if not rdv:
            QMessageBox.warning(
                self, "Erreur", "Sélectionnez un RDV"
            )
            return
        self.form = RDVForm(self.load_data, rdv)
        self.form.show()

    def delete_rdv(self):
        rdv = self.get_selected()
        if not rdv:
            return
        delete_rdv(rdv[0])
        self.load_data()
