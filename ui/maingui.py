from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                             QLineEdit, QLabel)

class YAILGui(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('YAIL - Yet Another AppImage Linker')
        self.setMinimumWidth(400)

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