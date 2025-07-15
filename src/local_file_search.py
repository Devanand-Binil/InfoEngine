import os
import fitz  # PyMuPDF
import markdown
import google.generativeai as genai
from docx import Document
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTextEdit,
    QFileDialog, QLabel, QMessageBox, QLineEdit, QHBoxLayout, QApplication
)
from PyQt5.QtCore import Qt


class LocalFileSearchWidget(QWidget):
    """
    Widget for scanning local files (PDF, DOCX, TXT) for a keyword,
    extracting matches, and summarizing results via Gemini.
    """

    def __init__(self):
        super().__init__()
        self.api_key = "AIzaSyCH6Q1RXbOukY0ZAVJDi3StqMst9x4xAVw"  # 🔐 Replace or load from env in production
        self.selected_folder = ""
        self._init_ui()

    def _init_ui(self):
        """Initializes layout and widgets."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.title = QLabel("📁 Local File Intelligence Scanner")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #1D3557;
        """)
        layout.addWidget(self.title)

        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("🔑 Enter keyword to search...")
        self.keyword_input.setMinimumHeight(32)
        self.keyword_input.setStyleSheet("""
            QLineEdit {
                padding: 6px 10px;
                font-size: 14px;
                border-radius: 6px;
                border: 1px solid #A8DADC;
            }
        """)
        layout.addWidget(self.keyword_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.select_folder_btn = QPushButton("📂 Choose Folder")
        self.select_folder_btn.clicked.connect(self.choose_folder)
        button_layout.addWidget(self.select_folder_btn)

        self.scan_button = QPushButton("🧠 Scan & Summarize")
        self.scan_button.clicked.connect(self.scan_documents)
        button_layout.addWidget(self.scan_button)
        layout.addLayout(button_layout)

        # Output display
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                color: #212529;
                padding: 10px;
                font-family: Consolas, monospace;
                font-size: 13px;
            }
        """)
        layout.addWidget(self.result_area)

    def choose_folder(self):
        """Prompts the user to select a folder."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.selected_folder = folder
            self.title.setText(f"📁 Scanning: {folder}")

    def perform_search(self, query):
        """For MainWindow compatibility: triggers scan with given query."""
        self.keyword_input.setText(query)
        self.scan_documents()

    def scan_documents(self):
        """Scans selected folder for keyword in text-based files and sends to summarizer."""
        keyword = self.keyword_input.text().strip().lower()

        if not self.selected_folder:
            QMessageBox.warning(self, "No Folder", "Please select a folder to scan.")
            return
        if not keyword:
            QMessageBox.warning(self, "No Keyword", "Please enter a keyword to search.")
            return

        self.result_area.setPlainText("🔍 Scanning files...")
        QApplication.processEvents()

        matched_text = ""

        for root, _, files in os.walk(self.selected_folder):
            for file in files:
                if file.endswith((".pdf", ".docx", ".txt")):
                    full_path = os.path.join(root, file)
                    content = self.extract_text_from_file(full_path)
                    if keyword in content.lower():
                        matched_text += f"\n\n📄 **{file}**:\n" + content + "\n"

        if not matched_text:
            self.result_area.setText("❌ No matches found for the given keyword.")
            return

        self.result_area.setText("🧠 Summarizing ...")
        QApplication.processEvents()

        summary = self.summarize_with_gemini(matched_text)
        html_summary = markdown.markdown(summary)
        self.result_area.setHtml(html_summary)

    def extract_text_from_file(self, file_path):
        """Extracts plain text from PDF, DOCX, or TXT file."""
        try:
            if file_path.endswith(".pdf"):
                text = ""
                doc = fitz.open(file_path)
                for page in doc:
                    text += page.get_text()
                return text

            elif file_path.endswith(".docx"):
                doc = Document(file_path)
                return "\n".join(para.text for para in doc.paragraphs)

            elif file_path.endswith(".txt"):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()

        except Exception as e:
            return f"[❗ Error reading {os.path.basename(file_path)}]: {e}"
        return ""

    def summarize_with_gemini(self, text):
        """Uses Gemini to summarize the matched text into a smart intelligence report."""
        try:
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""
You are an AI intelligence engine used by analysts to extract relevant insights from files.

Based on the content below, create a structured report. Adapt sections depending on whether it's about a person, event, or place.

Use bullet points. Keep it concise. Focus only on clear, factual information.

Text to analyze:
{text[:12000]}
"""

            response = model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            return f"❌ Gemini Error: {e}"
