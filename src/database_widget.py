from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QFrame, QLineEdit, QHeaderView
)
from PyQt5.QtCore import Qt, QTimer
import random


class DatabaseWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # --- Header Row ---
        header_layout = QHBoxLayout()

        title = QLabel("📚 Database Results")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #1D3557;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("🔍 Filter results...")
        self.filter_input.setStyleSheet("""
            QLineEdit {
                padding: 6px 10px;
                border: 1px solid #A8DADC;
                border-radius: 6px;
                font-size: 13px;
                background-color: #F8F9FA;
                max-width: 220px;
            }
        """)
        header_layout.addWidget(self.filter_input)

        self.export_button = QPushButton("Export CSV")
        self.export_button.setStyleSheet("""
            QPushButton {
                padding: 6px 14px;
                background-color: #1D3557;
                color: white;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #457B9D;
            }
            QPushButton:disabled {
                background-color: #A8DADC;
                color: #457B9D;
            }
        """)
        self.export_button.setEnabled(False)
        header_layout.addWidget(self.export_button)

        layout.addLayout(header_layout)

        # --- Status Panel ---
        self.status_frame = QFrame()
        self.status_frame.setStyleSheet("""
            background-color: #F1FAEE;
            border: 1px solid #A8DADC;
            border-radius: 8px;
            padding: 8px;
        """)
        status_layout = QVBoxLayout(self.status_frame)
        self.status_label = QLabel("✅ Database status: Connected")
        self.status_label.setStyleSheet("""
            color: #2A9D8F;
            font-weight: bold;
        """)
        status_layout.addWidget(self.status_label)
        layout.addWidget(self.status_frame)

        # --- Results Table ---
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Type", "Description"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #A8DADC;
                border-radius: 8px;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #457B9D;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QTableWidget::item:selected {
                background-color: #A8DADC;
                color: #1D3557;
            }
        """)
        layout.addWidget(self.table)

        # --- Signal connections ---
        self.filter_input.textChanged.connect(self.filter_results)
        self.export_button.clicked.connect(self.export_data)

        # --- Populate sample data initially ---
        self.populate_sample_data()

    def populate_sample_data(self):
        self.table.setRowCount(0)
        sample_data = [
            (1, "Document A", "PDF", "Annual financial report for 2024"),
            (2, "Research Paper", "DOC", "Analysis of market trends"),
            (3, "Product Spec", "XLSX", "Technical specifications"),
            (4, "Meeting Notes", "TXT", "Board meeting summary"),
            (5, "Legal Contract", "PDF", "Service agreement with vendor"),
            (6, "Quarterly Report", "PDF", "Q1 2024 performance overview"),
            (7, "Customer Data", "CSV", "Survey responses"),
            (8, "Marketing Plan", "PPTX", "Campaign strategy for Q3"),
            (9, "Budget Forecast", "XLSX", "Financial projections"),
            (10, "Employee Handbook", "PDF", "Company policies")
        ]
        for row_idx, (id_val, name, type_val, desc) in enumerate(sample_data):
            self._insert_row(row_idx, id_val, name, type_val, desc)
        self.export_button.setEnabled(True)

    def perform_search(self, query):
        self.status_label.setText(f"🔎 Searching for '{query}'...")
        self.status_label.setStyleSheet("color: #E63946; font-weight: bold;")
        self.table.setRowCount(0)
        self.export_button.setEnabled(False)
        QTimer.singleShot(1500, lambda: self.display_search_results(query))

    def display_search_results(self, query):
        self.status_label.setText(f"✅ Found results for '{query}'")
        self.status_label.setStyleSheet("color: #2A9D8F; font-weight: bold;")

        num_results = random.randint(2, 8)
        self.table.setRowCount(0)
        for i in range(num_results):
            id_val = 100 + i
            if i % 3 == 0:
                title = f"{query} Analysis Report"
            elif i % 3 == 1:
                title = f"Overview of {query}"
            else:
                title = f"{query} Reference Document"
            doc_type = ["PDF", "DOC", "XLSX", "TXT", "CSV"][i % 5]
            desc = [
                f"Detailed analysis of {query}",
                f"Historical data about {query}",
                f"Latest research findings",
                f"{query} implementation guide",
                f"Case studies involving {query}"
            ][i % 5]
            self._insert_row(i, id_val, title, doc_type, desc)
        self.export_button.setEnabled(True)

    def _insert_row(self, row_idx, id_val, name, type_val, desc):
        self.table.insertRow(row_idx)
        id_item = QTableWidgetItem(str(id_val))
        id_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row_idx, 0, id_item)
        self.table.setItem(row_idx, 1, QTableWidgetItem(name))
        type_item = QTableWidgetItem(type_val)
        type_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row_idx, 2, type_item)
        self.table.setItem(row_idx, 3, QTableWidgetItem(desc))

    def filter_results(self, text):
        text = text.lower()
        for row in range(self.table.rowCount()):
            hide_row = True
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and text in item.text().lower():
                    hide_row = False
                    break
            self.table.setRowHidden(row, hide_row)

    def export_data(self):
        visible_rows = sum(
            not self.table.isRowHidden(row) for row in range(self.table.rowCount())
        )
        self.status_label.setText(f"✅ Exported {visible_rows} records to CSV")
        self.status_label.setStyleSheet("color: #2A9D8F; font-weight: bold;")
        QTimer.singleShot(3000, lambda: self.status_label.setStyleSheet("color: #2A9D8F;"))
