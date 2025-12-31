from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox
)
from services.auth_service import authenticate

class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion – Cabinet de gynécologie")
        self.setFixedSize(350, 220)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Connexion")
        title.setStyleSheet("font-size:18px;font-weight:bold;")
        layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        login_btn = QPushButton("Se connecter")
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Erreur", "Tous les champs sont obligatoires")
            return

        user = authenticate(username, password)

        if user:
            from ui.dashboard.dashboard_window import DashboardWindow
            self.dashboard = DashboardWindow(user)
            self.dashboard.show()
            self.close()
            # 👉 plus tard : ouvrir le dashboard
        else:
            QMessageBox.critical(self, "Erreur", "Identifiants incorrects")
