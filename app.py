import sys
from PyQt6.QtWidgets import QApplication
from config.database import init_db
from ui.login.login_window import LoginWindow

init_db()

app = QApplication(sys.argv)
login = LoginWindow()
login.show()
sys.exit(app.exec())
