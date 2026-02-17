from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QHeaderView, QLabel)
from models.facture_model import FactureModel
from ui.facturation.facture_window import FactureWindow

class FacturationTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Barre d'outils
        tools = QHBoxLayout()
        title = QLabel("<h2>📁 Journal de Facturation</h2>")
        
        self.btn_ajouter = QPushButton("➕ Créer une Facture")
        self.btn_ajouter.setStyleSheet("background-color: #2980b9; color: white; padding: 10px; font-weight: bold;")
        self.btn_ajouter.clicked.connect(self.ouvrir_ajout)
        
        tools.addWidget(title)
        tools.addStretch()
        tools.addWidget(self.btn_ajouter)
        layout.addLayout(tools)

        # Tableau
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Référence", "Patiente", "Date", "Total", "Payé", "Reste"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
        
        self.refresh_table()

    def refresh_table(self):
        factures = FactureModel.get_all_factures()
        self.table.setRowCount(0)
        for f in factures:
            row = self.table.rowCount()
            self.table.insertRow(row)
            # On affiche les données de f[1] à f[6] (Réf, Nom, Date, Total, Payé, Reste)
            for i in range(1, 7):
                item = QTableWidgetItem(str(f[i]))
                self.table.setItem(row, i-1, item)

    def ouvrir_ajout(self):
        # On passe la méthode refresh_table pour mettre à jour la liste après l'ajout
        self.win = FactureWindow(refresh_callback=self.refresh_table)
        self.win.show()