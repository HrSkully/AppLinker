import sys
import os
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.maingui import YAILGui
from logic import create_desktop_file

class MainWindow(YAILGui):
    def __init__(self):
        super().__init__()
        # Signale verbinden
        self.btn_browse_app.clicked.connect(self.select_app)
        self.btn_browse_icon.clicked.connect(self.select_icon)
        self.btn_create.clicked.connect(self.run_logic)

    def select_app(self):
        file, _ = QFileDialog.getOpenFileName(self, "Wähle Datei")
        if file: self.path_input.setText(file)

    def select_icon(self):
        file, _ = QFileDialog.getOpenFileName(self, "Wähle Icon")
        if file: self.icon_input.setText(file)

    def run_logic(self):
        success, msg = create_desktop_file(
            self.name_input.text(),
            self.path_input.text(),
            self.icon_input.text()
        )
        if success:
            QMessageBox.information(self, "Erfolg", f"Erstellt: {msg}")
        else:
            QMessageBox.critical(self, "Fehler", msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())