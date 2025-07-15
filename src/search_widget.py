from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QRadioButton, QButtonGroup, QFileDialog, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal


class SearchWidget(QWidget):
    """
    Widget providing search input and facial recognition upload.
    Emits signals for search and image upload requests.
    """
    search_requested = pyqtSignal(str, str)  # query, search_type
    upload_requested = pyqtSignal(str)       # image_path

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self._create_title(layout)
        self._create_search_type_selector(layout)
        self._create_search_input_section(layout)
        self._create_upload_section(layout)

        layout.addStretch()

        self._connect_signals()

    def _create_title(self, layout):
        title = QLabel("Search Information")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1D3557;")
        layout.addWidget(title)

    def _create_search_type_selector(self, layout):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: #F1FAEE; border-radius: 8px; }")
        inner_layout = QVBoxLayout(frame)

        label = QLabel("Select Search Type:")
        label.setStyleSheet("font-weight: bold;")
        inner_layout.addWidget(label)

        self.web_radio = QRadioButton("Web Search")
        self.db_radio = QRadioButton("Database Search")
        self.local_radio = QRadioButton("Local Search")  # NEW
        self.face_radio = QRadioButton("Facial Recognition")

        self.web_radio.setChecked(True)

        self.search_type_group = QButtonGroup()
        for btn in (self.web_radio, self.db_radio, self.local_radio, self.face_radio):
            self.search_type_group.addButton(btn)

        radio_layout = QVBoxLayout()
        for btn in (self.web_radio, self.db_radio, self.local_radio, self.face_radio):
            radio_layout.addWidget(btn)
        inner_layout.addLayout(radio_layout)

        layout.addWidget(frame)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #A8DADC;")
        layout.addWidget(separator)

    def _create_search_input_section(self, layout):
        self.search_frame = QFrame()
        self.search_frame.setStyleSheet("QFrame { background-color: #F1FAEE; border-radius: 8px; }")
        form_layout = QVBoxLayout(self.search_frame)

        self.search_label = QLabel("Enter Search Query:")
        self.search_label.setStyleSheet("font-weight: bold;")
        form_layout.addWidget(self.search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type keywords, person name, etc...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #A8DADC;
                border-radius: 4px;
                background-color: white;
            }
        """)
        form_layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #457B9D;
                color: white;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1D3557;
            }
        """)
        form_layout.addWidget(self.search_button)

        layout.addWidget(self.search_frame)

    def _create_upload_section(self, layout):
        self.upload_frame = QFrame()
        self.upload_frame.setVisible(False)
        self.upload_frame.setStyleSheet("QFrame { background-color: #F1FAEE; border-radius: 8px; }")

        upload_layout = QVBoxLayout(self.upload_frame)

        label = QLabel("Upload Image for Facial Recognition:")
        label.setStyleSheet("font-weight: bold;")
        upload_layout.addWidget(label)

        self.upload_path_display = QLineEdit()
        self.upload_path_display.setReadOnly(True)
        self.upload_path_display.setPlaceholderText("No image selected...")
        self.upload_path_display.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #A8DADC;
                border-radius: 4px;
                background-color: white;
            }
        """)
        upload_layout.addWidget(self.upload_path_display)

        button_layout = QHBoxLayout()

        self.browse_button = QPushButton("Browse...")
        self.browse_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #A8DADC;
                color: #1D3557;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #457B9D;
                color: white;
            }
        """)

        self.upload_button = QPushButton("Process Image")
        self.upload_button.setEnabled(False)
        self.upload_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #E63946;
                color: white;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #C1121F;
            }
        """)

        button_layout.addWidget(self.browse_button)
        button_layout.addWidget(self.upload_button)

        upload_layout.addLayout(button_layout)
        layout.addWidget(self.upload_frame)

    def _connect_signals(self):
        self.search_button.clicked.connect(self.on_search)
        self.search_input.returnPressed.connect(self.on_search)
        self.browse_button.clicked.connect(self.browse_files)
        self.upload_button.clicked.connect(self.on_upload)
        self.face_radio.toggled.connect(self._toggle_upload_section)
        self.local_radio.toggled.connect(self._toggle_upload_section)  # Keep search input visible for local search

    def _toggle_upload_section(self, checked):
        """
        Toggle visibility of sections based on facial recognition radio button.
        Show search input for Web, Database, and Local searches.
        """
        if self.face_radio.isChecked():
            self.search_frame.setVisible(False)
            self.upload_frame.setVisible(True)
        else:
            self.search_frame.setVisible(True)
            self.upload_frame.setVisible(False)

    def on_search(self):
        """Emits a search_requested signal with the current input and type."""
        query = self.search_input.text().strip()
        if not query:
            return
        if self.web_radio.isChecked():
            search_type = "web"
        elif self.db_radio.isChecked():
            search_type = "database"
        elif self.local_radio.isChecked():
            search_type = "local"
        else:
            search_type = "web"

        self.search_requested.emit(query, search_type)

    def browse_files(self):
        """Opens a file dialog for image selection."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.upload_path_display.setText(file_path)
            self.upload_button.setEnabled(True)

    def on_upload(self):
        """Emits an upload_requested signal with the selected image path."""
        image_path = self.upload_path_display.text().strip()
        if image_path:
            self.upload_requested.emit(image_path)
            self.upload_button.setEnabled(False)
