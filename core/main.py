import subprocess
import sys
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox, QListWidgetItem

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.maingui import AppLinkerGui
from logic import create_desktop_file, get_installed_apps, delete_desktop_file
import ctypes
from PyQt6.QtGui import QIcon

__version__ = "1.2.0"

try:
    myappid = 'AppLinker.appimage.linker.v1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except AttributeError:
    pass

class MainWindow(AppLinkerGui):
    def __init__(self):
        super().__init__()

        self.version_label.setText(f"v{__version__}")

        self.btn_browse_app.clicked.connect(self.select_app)
        self.btn_browse_icon.clicked.connect(self.select_icon)
        self.btn_create.clicked.connect(self.run_logic)
        self.btn_refresh.clicked.connect(self.refresh_app_list)
        self.btn_delete.clicked.connect(self.delete_selected_app)

        self.refresh_app_list()

    def refresh_app_list(self):
        self.list_apps.clear()
        apps = get_installed_apps()
        for app in apps:
            item = QListWidgetItem(app['name'])
            item.setData(Qt.ItemDataRole.UserRole, app['path'])
            self.list_apps.addItem(item)

    def delete_selected_app(self):
        selected_item = self.list_apps.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Abbruch", "Bitte wähle eine App aus der Liste.")
            return

        file_path = selected_item.data(Qt.ItemDataRole.UserRole)
        confirm = QMessageBox.question(self, "Löschen", f"Möchtest du die Verknüpfung wirklich löschen?\n{file_path}")

        if confirm == QMessageBox.StandardButton.Yes:
            success, msg = delete_desktop_file(file_path)

            if success:
                QMessageBox.information(self, "Erfolg", "Verknüpfung und Icon wurden vollständig entfernt.")
                self.refresh_app_list()
            else:
                QMessageBox.critical(self, "Fehler", f"Löschen fehlgeschlagen: {msg}")

    def select_app(self):
        file, _ = QFileDialog.getOpenFileName(self, "Wähle Datei")
        if file: self.path_input.setText(file)

    def select_icon(self):
        file, _ = QFileDialog.getOpenFileName(self, "Wähle Icon")
        if file: self.icon_input.setText(file)

    def run_logic(self):
        app_name = self.name_input.text()
        app_path = self.path_input.text()
        icon_path = self.icon_input.text()

        description = self.desc_input.text() or "Created with AppLinker"

        wm_class = app_name.lower().replace(" ", "-")

        self.btn_create.setEnabled(False)
        self.btn_create.setText("Warte auf Autorisierung...")
        QApplication.processEvents()

        success, msg = create_desktop_file(
            app_name,
            app_path,
            icon_path,
            description,
            wm_class
        )

        self.btn_create.setEnabled(True)
        self.btn_create.setText("Systemweit registrieren")

        if success:
            QMessageBox.information(self, "Erfolg", f"Erstellt: {msg}")
            if hasattr(self, 'refresh_app_list'):
                self.refresh_app_list()
        else:
            QMessageBox.critical(self, "Fehler", msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icon_full_path = os.path.join(base_dir, 'icons', 'AppLinker_icon.png')

    if os.path.exists(icon_full_path):
        app.setWindowIcon(QIcon(icon_full_path))

    app.setApplicationName("AppLinker")
    app.setDesktopFileName("AppLinker.desktop")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())