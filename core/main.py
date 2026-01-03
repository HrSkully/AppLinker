import locale
import sys
import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox, QListWidgetItem
from i18n import TRANSLATIONS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.maingui import AppLinkerGui
from logic import create_desktop_file, get_installed_apps, delete_desktop_file, load_config, save_config
import ctypes
from PyQt6.QtGui import QIcon


__version__ = "1.3.0"

try:
    myappid = 'AppLinker.appimage.linker.v1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except AttributeError:
    pass

class MainWindow(AppLinkerGui):
    def __init__(self):
        super().__init__()
        self.config = load_config()

        if self.config.get("language"):
            self.lang_code = self.config["language"]
        else:
            try:
                self.lang_code = locale.getdefaultlocale()[0][:2]
            except:
                self.lang_code = 'en'

        self.texts = TRANSLATIONS.get(self.lang_code, TRANSLATIONS['en'])
        self.retranslate_ui()
        self.combo_lang.setCurrentIndex(0 if self.lang_code == 'de' else 1)

        self.combo_lang.currentIndexChanged.connect(self.change_language)
        self.version_label.setText(f"v{__version__}")

        self.btn_browse_app.clicked.connect(self.select_app)
        self.btn_browse_icon.clicked.connect(self.select_icon)
        self.btn_create.clicked.connect(self.run_logic)
        self.btn_refresh.clicked.connect(self.refresh_app_list)
        self.btn_delete.clicked.connect(self.delete_selected_app)

        self.refresh_app_list()

    def change_language(self):
        new_lang = 'de' if self.combo_lang.currentIndex() == 0 else 'en'
        self.lang_code = new_lang
        self.texts = TRANSLATIONS[new_lang]

        self.config["language"] = new_lang
        save_config(self.config)

        self.retranslate_ui()

    def retranslate_ui(self):
        """Aktualisiert alle Texte in der UI basierend auf self.texts"""

        self.combo_lang.blockSignals(True)
        current_idx = self.combo_lang.currentIndex()

        # Sprachauswahl Combobox
        self.combo_lang.clear()
        self.combo_lang.addItems([self.texts['lang_de'], self.texts['lang_en']])
        self.combo_lang.setCurrentIndex(current_idx)

        self.combo_lang.blockSignals(False)

        # Fenster & Tabs
        self.tabs.setTabText(0, self.texts['tab_create'])
        self.tabs.setTabText(1, self.texts['tab_manage'])

        # Erstellen Tab
        self.lbl_name.setText(self.texts['lbl_name'])
        self.lbl_desc.setText(self.texts['lbl_desc'])
        self.desc_input.setPlaceholderText(self.texts['ph_desc'])
        self.lbl_path.setText(self.texts['lbl_path'])
        self.btn_browse_app.setText(self.texts['btn_browse'])
        self.lbl_icon.setText(self.texts['lbl_icon'])
        self.btn_browse_icon.setText(self.texts['btn_icon'])
        self.btn_create.setText(self.texts['btn_register'])

        # Verwalten Tab
        self.lbl_list.setText(self.texts['lbl_list'])
        self.btn_refresh.setText(self.texts['btn_refresh'])
        self.btn_delete.setText(self.texts['btn_delete'])

        # Sprachauswahl Combobox


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
        self.btn_create.setText(self.texts['msg_wait'])
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