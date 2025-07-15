from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QSplitter, QLabel, QStatusBar, QPushButton,
    QLineEdit, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt

from .search_widget import SearchWidget
from .results_widget import ResultsWidget
from .database_widget import DatabaseWidget
from .facial_recognition import MainApp as FacialRecognitionWidget
from .local_file_search import LocalFileSearchWidget


class MainWindow(QMainWindow):
    """
    Main window for the Information Engine app.
    Contains header, sidebar tools, tabbed search results, and status bar.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Information Engine")
        self.setMinimumSize(1200, 800)
        self._init_ui()

    def _init_ui(self):
        """Initializes layout and subcomponents."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self._setup_header()
        self._setup_content()
        self._setup_status_bar()

    def _setup_header(self):
        """Creates the app header with title, theme toggle, and global search bar."""

        # App title + theme toggle
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 10, 10)

        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)
        title_row.setSpacing(10)

        title_row.addStretch()
        title_label = QLabel("\U0001F9E0 Information Engine")
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #1D3557;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        title_row.addWidget(title_label)
        title_row.addStretch()

        self.theme_toggle = QPushButton("\U0001F319")
        self.theme_toggle.setToolTip("Toggle Dark/Light Mode")
        self.theme_toggle.setFixedSize(32, 32)
        self.theme_toggle.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 18px;
            }
            QPushButton:hover {
                color: #E63946;
            }
        """)
        self.theme_toggle.clicked.connect(self._toggle_theme)
        title_row.addWidget(self.theme_toggle)

        header_layout.addLayout(title_row)

        # Global search bar row
        search_row = QHBoxLayout()
        search_row.setContentsMargins(0, 0, 10, 0)
        search_row.setSpacing(10)

        self.global_search_input = QLineEdit()
        self.global_search_input.setPlaceholderText("\U0001F50D Search all sources (Google, DB, Local)...")
        self.global_search_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.global_search_input.setMinimumHeight(36)
        self.global_search_input.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 6px 12px;
                border-radius: 6px;
                border: 1px solid #A8DADC;
                background-color: #f8f9fa;
            }
        """)
        search_row.addWidget(self.global_search_input)

        self.global_search_button = QPushButton("Search All")
        self.global_search_button.setFixedHeight(36)
        self.global_search_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                padding: 6px 16px;
                border-radius: 6px;
                background-color: #1D3557;
                color: white;
            }
            QPushButton:hover {
                background-color: #457B9D;
            }
        """)
        self.global_search_button.clicked.connect(self._handle_global_search)
        search_row.addWidget(self.global_search_button)

        header_layout.addLayout(search_row)

        self.main_layout.addWidget(header)

    def _setup_content(self):
        """Sets up the main splitter layout: search tools and result tabs."""
        self.content_splitter = QSplitter(Qt.Horizontal)

        # Sidebar search tools
        self.search_widget = SearchWidget()
        self.content_splitter.addWidget(self.search_widget)

        # Tabbed result panels
        self.results_tabs = QTabWidget()
        self.results_tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.google_results = ResultsWidget("Google Search")
        self.results_tabs.addTab(self.google_results, "\U0001F310 Google Results")

        self.db_widget = DatabaseWidget()
        self.results_tabs.addTab(self.db_widget, "\U0001F4CA Database Results")

        self.facial_widget = FacialRecognitionWidget()
        self.results_tabs.addTab(self.facial_widget, "\U0001F9EC Facial Recognition")

        self.local_file_search = LocalFileSearchWidget()
        self.results_tabs.addTab(self.local_file_search, "\U0001F4C1 Local Search")

        self.content_splitter.addWidget(self.results_tabs)
        self.content_splitter.setStretchFactor(1, 3)
        self.content_splitter.setSizes([350, 850])

        self.main_layout.addWidget(self.content_splitter)

        # Connect sidebar signals
        self.search_widget.search_requested.connect(self.handle_search)
        self.search_widget.upload_requested.connect(self.handle_upload)

    def _setup_status_bar(self):
        """Initializes the bottom status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("\u2705 Ready")

    def _toggle_theme(self):
        """Placeholder slot for toggling theme (can be extended later)."""
        self.status_bar.showMessage("\U0001F319 Theme toggle clicked (Not yet implemented)")

    def _handle_global_search(self):
        """Handles global search request across all data sources."""
        query = self.global_search_input.text().strip()
        if not query:
            self.status_bar.showMessage("\u26A0\uFE0F Enter a keyword to search.")
            return

        self.status_bar.showMessage(f"\U0001F50D Running global search for: '{query}'")
        self.google_results.perform_search(query)
        self.db_widget.perform_search(query)
        self.local_file_search.perform_search(query)

        self.results_tabs.setCurrentWidget(self.google_results)

    def handle_search(self, query: str, search_type: str):
        """Routes individual searches to appropriate tab."""
        self.status_bar.showMessage(f"Searching for: {query}")

        if search_type == "web":
            self.google_results.perform_search(query)
            self.results_tabs.setCurrentWidget(self.google_results)
        elif search_type == "database":
            self.db_widget.perform_search(query)
            self.results_tabs.setCurrentWidget(self.db_widget)
        elif search_type == "local":
            self.local_file_search.perform_search(query)
            self.results_tabs.setCurrentWidget(self.local_file_search)

    def handle_upload(self, image_path: str):
        """Handles uploaded image path for face recognition."""
        self.status_bar.showMessage(f"\U0001F5BC\uFE0F Processing image: {image_path}")
        self.facial_widget.process_image(image_path)
        self.results_tabs.setCurrentWidget(self.facial_widget)
