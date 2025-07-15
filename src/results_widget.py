# src/results_widget.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSlot
import time


class ResultsWidget(QWidget):
    def __init__(self, title="Search Results"):
        super().__init__()
        self.setWindowTitle(title)
        self.query_pending = None

        self.view = QWebEngineView()
        self.view.loadFinished.connect(self.on_page_loaded)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        # Cache-busting trick to avoid old HTML being used
        timestamp = int(time.time())
        self.view.load(QUrl(f"http://localhost:8765?ts={timestamp}"))

    def perform_search(self, query):
        """Queue a query for when the page is ready."""
        self.query_pending = query
        self.try_execute_query()

    @pyqtSlot(bool)
    def on_page_loaded(self, ok):
        if ok:
            self.try_execute_query()
        else:
            print("❌ Failed to load search page")

    def try_execute_query(self):
        """Try running the query if the page and JS are ready."""
        if self.query_pending:
            # Ensure autoSearch exists before calling
            js = f"""
                if (typeof autoSearch === 'function') {{
                    autoSearch({repr(self.query_pending)});
                }} else {{
                    console.warn("autoSearch not yet available");
                }}
            """
            self.view.page().runJavaScript(js)
            self.query_pending = None
