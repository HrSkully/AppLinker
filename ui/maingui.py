import locale
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLineEdit, QLabel, QTabWidget, QListWidget, QComboBox)
from core.i18n import TRANSLATIONS

class AppLinkerGui(QWidget):
    """
    Base GUI class for AppLinker.
    Defines the visual layout, widgets, and initial language setup.
    """

    def __init__(self):
        super().__init__()

        # Automatic language detection based on system locale
        try:
            self.lang_code = locale.getdefaultlocale()[0][:2]
        except (AttributeError, IndexError):
            # Fallback to English if detection fails
            self.lang_code = 'en'

        # Load dictionary for the detected language
        self.texts = TRANSLATIONS.get(self.lang_code, TRANSLATIONS['en'])

        # Basic window configuration
        self.setWindowTitle('AppLinker')
        self.setMinimumWidth(520)
        self.setMinimumHeight(480)

        # Main vertical layout container
        self.main_layout = QVBoxLayout()

        # --- TOP BAR (Language Selection) ---

        top_bar = QHBoxLayout()

        # Bug Report Button
        self.btn_bug = QPushButton("🪲")
        self.btn_bug.setFixedSize(30, 30)
        self.btn_bug.setToolTip("Report a Bug / Request Feature")
        self.btn_bug.setStyleSheet("QPushButton { border: none; font-size: 16px; } QPushButton:hover { border-radius: 5px; }")

        # Provides a dropdown menu for manual language override
        self.combo_lang = QComboBox()
        self.combo_lang.addItems([self.texts['lang_de'], self.texts['lang_en']])
        self.combo_lang.setCurrentIndex(0 if self.lang_code == 'de' else 1)

        top_bar.addStretch()
        top_bar.addWidget(QLabel("🌐"))
        top_bar.addWidget(self.combo_lang)
        self.main_layout.addLayout(top_bar)

        # Tab widget for separating "Creation" and "Management" views
        self.tabs = QTabWidget()

        # --- TAB 1: CREATE SHORTCUT ---
        # UI components for entering application metadata and executable paths
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

        # Assembling the creation layout
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

        # --- TAB 2: MANAGE SHORTCUTS ---
        # UI components for listing and deleting existing AppLinker entries
        self.tab_manage = QWidget()
        manage_layout = QVBoxLayout()

        self.lbl_list = QLabel(self.texts['lbl_list'])
        self.list_apps = QListWidget()

        button_layout = QHBoxLayout()
        self.btn_refresh = QPushButton(self.texts['btn_refresh'])
        self.btn_delete = QPushButton(self.texts['btn_delete'])
        # Highlight delete button with red background for safety awareness
        self.btn_delete.setStyleSheet("background-color: #c0392b; color: white;")

        button_layout.addWidget(self.btn_refresh)
        button_layout.addWidget(self.btn_delete)

        manage_layout.addWidget(self.lbl_list)
        manage_layout.addWidget(self.list_apps)
        manage_layout.addLayout(button_layout)
        self.tab_manage.setLayout(manage_layout)

        # Finalizing tab addition
        self.tabs.addTab(self.tab_create, self.texts['tab_create'])
        self.tabs.addTab(self.tab_manage, self.texts['tab_manage'])

        self.main_layout.addWidget(self.tabs)

        # --- STATUS BAR ---
        # Displays the current software version at the bottom right
        self.status_layout = QHBoxLayout()
        self.version_label = QLabel('')
        self.version_label.setStyleSheet("color: gray; font-size: 10px;")

        self.status_layout.addWidget(self.btn_bug)
        self.status_layout.addStretch()
        self.status_layout.addWidget(self.version_label)
        self.main_layout.addLayout(self.status_layout)

        self.setLayout(self.main_layout)