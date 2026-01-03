import os
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel

class AppLinkerGui(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AppLinker')
        self.setMinimumWidth(500)
        self.setMinimumHeight(200)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, 'icons', 'AppLinker_icon.png')

        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout()

        layout.addWidget(QLabel('Name der Anwendung:'))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel('Pfad zur ausführbaren Datei:'))
        self.path_input = QLineEdit()
        self.btn_browse_app = QPushButton('Datei wählen')
        layout.addWidget(self.path_input)
        layout.addWidget(self.btn_browse_app)

        layout.addWidget(QLabel('Icon Pfad:'))
        self.icon_input = QLineEdit()
        self.btn_browse_icon = QPushButton('Icon wählen')
        layout.addWidget(self.icon_input)
        layout.addWidget(self.btn_browse_icon)

        self.btn_create = QPushButton('Systemweit registrieren')
        layout.addWidget(self.btn_create)

        self.setLayout(layout)