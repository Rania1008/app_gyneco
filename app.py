import sys
from PyQt6.QtWidgets import QApplication
from config.database import init_db
from ui.login.login_window import LoginWindow

def main():
    # 1. On initialise/met à jour la base de données avant de lancer l'UI
    init_db()

    # 2. Lancement de l'application PyQt
    app = QApplication(sys.argv)
    
    # On commence par la fenêtre de login
    login = LoginWindow()
    login.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()