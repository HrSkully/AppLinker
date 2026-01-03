import locale
import sys
import os
import ctypes
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox, QListWidgetItem

# Add the parent directory to the system path to ensure modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from i18n import TRANSLATIONS
from ui.maingui import AppLinkerGui
from logic import (create_desktop_file, get_installed_apps, delete_desktop_file,
                   load_config, save_config)

__version__ = "1.3.1"

# Attempt to set a unique AppUserModelID for Windows taskbar grouping
try:
    myappid = 'AppLinker.appimage.linker.v1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except AttributeError:
    # This call is only relevant on Windows systems
    pass


class MainWindow(AppLinkerGui):
    """
    Main application logic and controller.
    Inherits from AppLinkerGui and connects user interface actions to logic functions.
    """

    def __init__(self):
        # Initialize basic UI structure from the parent class
        super().__init__()

        self.version_label.setText(f"v{__version__}")

        # Load user configuration and determine the active language
        self.config = load_config()
        if self.config.get("language"):
            self.lang_code = self.config["language"]
        else:
            try:
                # Detect system language as fallback
                self.lang_code = locale.getdefaultlocale()[0][:2]
            except (AttributeError, IndexError):
                self.lang_code = 'en'

        # Set initial translation dictionary
        self.texts = TRANSLATIONS.get(self.lang_code, TRANSLATIONS['en'])

        # Apply language settings to the UI and initialize the dropdown state
        self.retranslate_ui()
        self.combo_lang.blockSignals(True)
        self.combo_lang.setCurrentIndex(0 if self.lang_code == 'de' else 1)
        self.combo_lang.blockSignals(False)

        # UI signals and slots connections
        self.combo_lang.currentIndexChanged.connect(self.change_language)
        self.version_label.setText(f"v{__version__}")
        self.btn_browse_app.clicked.connect(self.select_app)
        self.btn_browse_icon.clicked.connect(self.select_icon)
        self.btn_create.clicked.connect(self.run_logic)
        self.btn_refresh.clicked.connect(self.refresh_app_list)
        self.btn_delete.clicked.connect(self.delete_selected_app)

        # Initial load of installed applications
        self.refresh_app_list()

    def change_language(self):
        """
        Handles manual language switching via the dropdown menu.
        Updates the configuration and triggers a UI retranslation.
        """
        new_lang = 'de' if self.combo_lang.currentIndex() == 0 else 'en'
        self.lang_code = new_lang
        self.texts = TRANSLATIONS[new_lang]

        # Persist the choice in the local config file
        self.config["language"] = new_lang
        save_config(self.config)

        self.retranslate_ui()

    def retranslate_ui(self):
        """
        Updates all static and dynamic text elements in the user interface.
        """
        # Update language selector dropdown while preventing signal loops
        self.combo_lang.blockSignals(True)
        current_idx = self.combo_lang.currentIndex()
        self.combo_lang.clear()
        self.combo_lang.addItems([self.texts['lang_de'], self.texts['lang_en']])
        self.combo_lang.setCurrentIndex(current_idx)
        self.combo_lang.blockSignals(False)

        # Main window and tab titles
        self.tabs.setTabText(0, self.texts['tab_create'])
        self.tabs.setTabText(1, self.texts['tab_manage'])

        # Input labels and button texts for the "Create" tab
        self.lbl_name.setText(self.texts['lbl_name'])
        self.lbl_desc.setText(self.texts['lbl_desc'])
        self.desc_input.setPlaceholderText(self.texts['ph_desc'])
        self.lbl_path.setText(self.texts['lbl_path'])
        self.btn_browse_app.setText(self.texts['btn_browse'])
        self.lbl_icon.setText(self.texts['lbl_icon'])
        self.btn_browse_icon.setText(self.texts['btn_icon'])
        self.btn_create.setText(self.texts['btn_register'])

        # Texts for the "Manage" tab
        self.lbl_list.setText(self.texts['lbl_list'])
        self.btn_refresh.setText(self.texts['btn_refresh'])
        self.btn_delete.setText(self.texts['btn_delete'])

    def refresh_app_list(self):
        """
        Scans for installed shortcuts and updates the QListWidget view.
        """
        self.list_apps.clear()
        apps = get_installed_apps()
        for app in apps:
            item = QListWidgetItem(app['name'])
            # Store the underlying file path as user data for easier deletion later
            item.setData(Qt.ItemDataRole.UserRole, app['path'])
            self.list_apps.addItem(item)

    def delete_selected_app(self):
        """
        Initiates the deletion process for the currently selected list item.
        Prompts for confirmation before removing system files.
        """
        selected_item = self.list_apps.currentItem()
        if not selected_item:
            return

        file_path = selected_item.data(Qt.ItemDataRole.UserRole)
        confirm = QMessageBox.question(self, "Delete", f"Really delete this shortcut?\n{file_path}")

        if confirm == QMessageBox.StandardButton.Yes:
            success, msg = delete_desktop_file(file_path)
            if success:
                QMessageBox.information(self, "Success", "Shortcut and icon removed.")
                self.refresh_app_list()
            else:
                QMessageBox.critical(self, "Error", f"Deletion failed: {msg}")

    def select_app(self):
        """Opens a file dialog to select the target executable."""
        file, _ = QFileDialog.getOpenFileName(self, "Select Executable")
        if file: self.path_input.setText(file)

    def select_icon(self):
        """Opens a file dialog to select an application icon."""
        file, _ = QFileDialog.getOpenFileName(self, "Select Icon")
        if file: self.icon_input.setText(file)

    def run_logic(self):
        """
        Gathers input data and executes the shortcut creation logic.
        Updates the UI state during processing to provide feedback.
        """
        app_name = self.name_input.text()
        app_path = self.path_input.text()
        icon_path = self.icon_input.text()
        description = self.desc_input.text() or "Created with AppLinker"
        wm_class = app_name.lower().replace(" ", "-")

        # Visual feedback during the pkexec process
        self.btn_create.setEnabled(False)
        self.btn_create.setText(self.texts.get('msg_wait', 'Processing...'))
        QApplication.processEvents()

        success, msg = create_desktop_file(
            app_name, app_path, icon_path, description, wm_class
        )

        # Re-enable UI components after processing
        self.btn_create.setEnabled(True)
        self.btn_create.setText(self.texts['btn_register'])

        if success:
            QMessageBox.information(self, "Success", f"Shortcut created: {msg}")
            self.refresh_app_list()
        else:
            QMessageBox.critical(self, "Error", msg)


if __name__ == '__main__':
    # Initialize the main application instance
    app = QApplication(sys.argv)

    # Set the application-wide icon
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icon_full_path = os.path.join(base_dir, 'icons', 'AppLinker_icon.png')
    if os.path.exists(icon_full_path):
        app.setWindowIcon(QIcon(icon_full_path))

    app.setApplicationName("AppLinker")
    app.setDesktopFileName("AppLinker.desktop")

    # Launch the main window
    window = MainWindow()
    window.show()
    sys.exit(app.exec())