import os
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLineEdit, QLabel, QTabWidget, QListWidget)


class AppLinkerGui(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AppLinker')
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, 'icons', 'AppLinker_icon.png')

        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Hauptlayout mit Tabs
        self.main_layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # --- TAB 1: ERSTELLEN ---
        self.tab_create = QWidget()
        create_layout = QVBoxLayout()

        create_layout.addWidget(QLabel('Name der Anwendung:'))
        self.name_input = QLineEdit()
        create_layout.addWidget(self.name_input)

        create_layout.addWidget(QLabel('Beschreibung (optional):'))
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText('z.B. Mein lieblings Grafikprogramm')
        create_layout.addWidget(self.desc_input)

        create_layout.addWidget(QLabel('Pfad zur ausführbaren Datei:'))
        self.path_input = QLineEdit()
        self.btn_browse_app = QPushButton('Datei wählen')
        create_layout.addWidget(self.path_input)
        create_layout.addWidget(self.btn_browse_app)

        create_layout.addWidget(QLabel('Icon Pfad:'))
        self.icon_input = QLineEdit()
        self.btn_browse_icon = QPushButton('Icon wählen')
        create_layout.addWidget(self.icon_input)
        create_layout.addWidget(self.btn_browse_icon)

        self.btn_create = QPushButton('Systemweit registrieren')
        create_layout.addStretch()
        create_layout.addWidget(self.btn_create)
        self.tab_create.setLayout(create_layout)

        # --- TAB 2: VERWALTEN ---
        self.tab_manage = QWidget()
        manage_layout = QVBoxLayout()

        manage_layout.addWidget(QLabel('Erstellte Verknüpfungen:'))
        self.list_apps = QListWidget()
        manage_layout.addWidget(self.list_apps)

        button_layout = QHBoxLayout()
        self.btn_refresh = QPushButton('Liste aktualisieren')
        self.btn_delete = QPushButton('Ausgewählte löschen')
        self.btn_delete.setStyleSheet("background-color: #c0392b; color: white;")

        button_layout.addWidget(self.btn_refresh)
        button_layout.addWidget(self.btn_delete)
        manage_layout.addLayout(button_layout)

        self.tab_manage.setLayout(manage_layout)

        # Tabs hinzufügen
        self.tabs.addTab(self.tab_create, "Erstellen")
        self.tabs.addTab(self.tab_manage, "Verwalten")

        self.main_layout.addWidget(self.tabs)
        self.setLayout(self.main_layout)

        # --- STATUSBAR ---
        self.status_layout = QHBoxLayout()
        self.version_label = QLabel('v1.2.0')
        self.version_label.setStyleSheet("color: gray; font-size: 10px;")

        self.status_layout.addStretch()
        self.status_layout.addWidget(self.version_label)

        self.main_layout.addLayout(self.status_layout)
        self.setLayout(self.main_layout)