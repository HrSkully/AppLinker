import locale
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLineEdit, QLabel, QTabWidget, QListWidget, QComboBox)
from core.i18n import TRANSLATIONS


class AppLinkerGui(QWidget):
    def __init__(self):
        super().__init__()

        # Initialer Sprach-Check
        try:
            self.lang_code = locale.getdefaultlocale()[0][:2]
        except:
            self.lang_code = 'en'

        self.texts = TRANSLATIONS.get(self.lang_code, TRANSLATIONS['en'])

        self.setWindowTitle('AppLinker')
        self.setMinimumWidth(520)
        self.setMinimumHeight(480)

        self.main_layout = QVBoxLayout()

        # --- TOP BAR (Sprachumschalter) ---
        top_bar = QHBoxLayout()
        self.combo_lang = QComboBox()
        self.combo_lang.addItems(['Deutsch', 'English'])
        self.combo_lang.setCurrentIndex(0 if self.lang_code == 'de' else 1)

        top_bar.addStretch()
        top_bar.addWidget(QLabel("🌐"))
        top_bar.addWidget(self.combo_lang)
        self.main_layout.addLayout(top_bar)

        self.tabs = QTabWidget()

        # --- TAB 1: ERSTELLEN ---
        self.tab_create = QWidget()
        create_layout = QVBoxLayout()

        self.lbl_name = QLabel(self.texts['lbl_name'])
        self.name_input = QLineEdit()

        self.lbl_desc = QLabel(self.texts['lbl_desc'])
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText(self.texts['ph_desc'])

        self.lbl_path = QLabel(self.texts['lbl_path'])
        self.path_input = QLineEdit()
        self.btn_browse_app = QPushButton(self.texts['btn_browse'])

        self.lbl_icon = QLabel(self.texts['lbl_icon'])
        self.icon_input = QLineEdit()
        self.btn_browse_icon = QPushButton(self.texts['btn_icon'])

        self.btn_create = QPushButton(self.texts['btn_register'])

        # Widgets hinzufügen
        create_layout.addWidget(self.lbl_name)
        create_layout.addWidget(self.name_input)
        create_layout.addWidget(self.lbl_desc)
        create_layout.addWidget(self.desc_input)
        create_layout.addWidget(self.lbl_path)
        create_layout.addWidget(self.path_input)
        create_layout.addWidget(self.btn_browse_app)
        create_layout.addWidget(self.lbl_icon)
        create_layout.addWidget(self.icon_input)
        create_layout.addWidget(self.btn_browse_icon)
        create_layout.addStretch()
        create_layout.addWidget(self.btn_create)
        self.tab_create.setLayout(create_layout)

        # --- TAB 2: VERWALTEN ---
        self.tab_manage = QWidget()
        manage_layout = QVBoxLayout()

        self.lbl_list = QLabel(self.texts['lbl_list'])
        self.list_apps = QListWidget()

        button_layout = QHBoxLayout()
        self.btn_refresh = QPushButton(self.texts['btn_refresh'])
        self.btn_delete = QPushButton(self.texts['btn_delete'])
        self.btn_delete.setStyleSheet("background-color: #c0392b; color: white;")
        button_layout.addWidget(self.btn_refresh)
        button_layout.addWidget(self.btn_delete)

        manage_layout.addWidget(self.lbl_list)
        manage_layout.addWidget(self.list_apps)
        manage_layout.addLayout(button_layout)
        self.tab_manage.setLayout(manage_layout)

        # Tabs hinzufügen
        self.tabs.addTab(self.tab_create, self.texts['tab_create'])
        self.tabs.addTab(self.tab_manage, self.texts['tab_manage'])

        self.main_layout.addWidget(self.tabs)

        # --- STATUSBAR ---
        self.status_layout = QHBoxLayout()
        self.version_label = QLabel('v1.3.0')
        self.version_label.setStyleSheet("color: gray; font-size: 10px;")
        self.status_layout.addStretch()
        self.status_layout.addWidget(self.version_label)
        self.main_layout.addLayout(self.status_layout)

        self.setLayout(self.main_layout)