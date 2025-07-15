#src/facial_recognition.py
import os
import sqlite3
import face_recognition
import pickle
import shutil

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox,
    QHBoxLayout, QLineEdit, QStackedWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QGroupBox, QFormLayout, QTextEdit, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont

DATABASE_PATH = "people.db"
ENCODINGS_DIR = "encodings"
PHOTOS_DIR = "photos"


def init_database():
    if not os.path.exists(DATABASE_PATH):
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                info TEXT
            )
        """)
        conn.commit()
        conn.close()

    os.makedirs(ENCODINGS_DIR, exist_ok=True)
    os.makedirs(PHOTOS_DIR, exist_ok=True)


class AddPersonPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.setContentsMargins(40, 40, 40, 20)
        layout.setSpacing(15)

        self.name_input = QLineEdit()
        self.info_input = QLineEdit()

        for inp in [self.name_input, self.info_input]:
            inp.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 6px;")

        self.image_button = QPushButton("📷 Select Image")
        self.image_button.clicked.connect(self.select_image)
        self.image_button.setStyleSheet("padding: 8px; background-color: #457B9D; color: white; border-radius: 6px;")

        self.save_button = QPushButton("💾 Save Person")
        self.save_button.clicked.connect(self.save_person)
        self.save_button.setStyleSheet("padding: 8px; background-color: #2A9D8F; color: white; border-radius: 6px;")

        layout.addRow("Name:", self.name_input)
        layout.addRow("Info:", self.info_input)
        layout.addRow("Image:", self.image_button)
        layout.addRow(self.save_button)

        self.setLayout(layout)
        self.selected_image_path = None

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.jpg *.jpeg *.png)")
        if path:
            self.selected_image_path = path
            self.image_button.setText(f"📸 {os.path.basename(path)}")

    def save_person(self):
        name = self.name_input.text().strip()
        info = self.info_input.text().strip()
        if not name or not info or not self.selected_image_path:
            QMessageBox.warning(self, "Missing Data", "Please fill all fields and select an image.")
            return

        image = face_recognition.load_image_file(self.selected_image_path)
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            QMessageBox.critical(self, "Face Error", "No face found in the image.")
            return

        encoding = encodings[0]
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO people (name, info) VALUES (?, ?)", (name, info))
        person_id = c.lastrowid
        conn.commit()
        conn.close()

        with open(f"{ENCODINGS_DIR}/{person_id}.pkl", "wb") as f:
            pickle.dump(encoding, f)

        target_name = f"{PHOTOS_DIR}/{person_id}_{os.path.basename(self.selected_image_path)}"
        shutil.copy(self.selected_image_path, target_name)

        QMessageBox.information(self, "Saved", "Person added successfully.")
        self.name_input.clear()
        self.info_input.clear()
        self.image_button.setText("📷 Select Image")
        self.selected_image_path = None


class ModifyPersonPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Info"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("QTableWidget { border: 1px solid #ccc; border-radius: 8px; }")
        self.layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.delete_button = QPushButton("🗑 Delete Selected")
        self.delete_button.clicked.connect(self.delete_selected)
        self.refresh_button = QPushButton("🔄 Refresh")
        self.refresh_button.clicked.connect(self.load_people)

        for btn in [self.delete_button, self.refresh_button]:
            btn.setStyleSheet("padding: 6px 12px; border-radius: 6px; background-color: #E76F51; color: white;")

        btn_layout.addStretch()
        btn_layout.addWidget(self.delete_button)
        btn_layout.addWidget(self.refresh_button)
        self.layout.addLayout(btn_layout)

        self.setLayout(self.layout)
        self.load_people()

    def load_people(self):
        self.table.setRowCount(0)
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        for row_idx, row in enumerate(c.execute("SELECT id, name, info FROM people")):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        conn.close()

    def delete_selected(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
        row = selected_items[0].row()
        person_id = int(self.table.item(row, 0).text())

        confirm = QMessageBox.question(self, "Confirm Delete", f"Delete person ID {person_id}?")
        if confirm != QMessageBox.Yes:
            return

        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM people WHERE id = ?", (person_id,))
        conn.commit()
        conn.close()

        os.remove(f"{ENCODINGS_DIR}/{person_id}.pkl") if os.path.exists(f"{ENCODINGS_DIR}/{person_id}.pkl") else None
        for fname in os.listdir(PHOTOS_DIR):
            if fname.startswith(f"{person_id}_"):
                os.remove(os.path.join(PHOTOS_DIR, fname))

        self.load_people()


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        init_database()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        nav = QHBoxLayout()
        self.add_btn = QPushButton("➕ Add Person")
        self.modify_btn = QPushButton("📝 Modify Person")
        self.theme_btn = QPushButton("🌙")

        for btn in [self.add_btn, self.modify_btn]:
            btn.setStyleSheet("padding: 8px 16px; font-weight: bold; border-radius: 6px; background-color: #264653; color: white;")

        self.theme_btn.setFixedSize(32, 32)
        self.theme_btn.setToolTip("Toggle Theme")
        self.theme_btn.setStyleSheet("border-radius: 16px; background-color: #A8DADC; color: black;")

        self.add_btn.clicked.connect(self.show_add_page)
        self.modify_btn.clicked.connect(self.show_modify_page)
        self.theme_btn.clicked.connect(self.toggle_theme)

        nav.addWidget(self.add_btn)
        nav.addWidget(self.modify_btn)
        nav.addStretch()
        nav.addWidget(self.theme_btn)
        self.layout.addLayout(nav)

        self.stack = QStackedWidget()
        self.add_page = AddPersonPage()
        self.modify_page = ModifyPersonPage()
        self.stack.addWidget(self.add_page)
        self.stack.addWidget(self.modify_page)
        self.layout.addWidget(self.stack)

        self.result_box = QGroupBox("🎯 Match Result")
        result_layout = QHBoxLayout()
        self.result_image = QLabel()
        self.result_image.setFixedSize(160, 160)
        self.result_image.setStyleSheet("border: 1px solid #ccc; border-radius: 8px;")
        self.result_image.setScaledContents(True)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("padding: 8px; font-family: monospace;")

        result_layout.addWidget(self.result_image)
        result_layout.addWidget(self.result_text)
        self.result_box.setLayout(result_layout)
        self.result_box.setVisible(False)

        self.layout.addWidget(self.result_box)
        self.setLayout(self.layout)

        self.current_theme = "light"
        self.apply_theme()

    def show_add_page(self):
        self.stack.setCurrentWidget(self.add_page)

    def show_modify_page(self):
        self.stack.setCurrentWidget(self.modify_page)

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()

    def apply_theme(self):
        if self.current_theme == "dark":
            self.setStyleSheet("""
                QWidget { background-color: #1E1E1E; color: #FFFFFF; }
                QPushButton { background-color: #444; color: white; border: 1px solid #888; padding: 6px; }
                QPushButton:hover { background-color: #666; }
                QLineEdit, QTextEdit {
                    background-color: #333; color: white; border: 1px solid #888;
                }
                QTableWidget { background-color: #2E2E2E; color: white; }
            """)
        else:
            self.setStyleSheet("")

    def process_image(self, image_path):
        try:
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if not encodings:
                QMessageBox.warning(self, "No Face", "No recognizable face found.")
                return

            input_encoding = encodings[0]
            conn = sqlite3.connect(DATABASE_PATH)
            c = conn.cursor()
            matches = []

            for row in c.execute("SELECT id, name, info FROM people"):
                pid, name, info = row
                encoding_path = os.path.join(ENCODINGS_DIR, f"{pid}.pkl")
                if os.path.exists(encoding_path):
                    with open(encoding_path, "rb") as f:
                        known_encoding = pickle.load(f)
                        match = face_recognition.compare_faces([known_encoding], input_encoding)[0]
                        if match:
                            matches.append((pid, name, info))
            conn.close()

            if matches:
                pid, name, info = matches[0]
                stored_image_path = self._find_image_for_person(pid)
                self.result_box.setVisible(True)
                self.result_text.setPlainText(f"👤 Name: {name}\n📝 Info: {info}")
                if stored_image_path:
                    self.result_image.setPixmap(QPixmap(stored_image_path))
                else:
                    self.result_image.setText("Image\nNot\nFound")
            else:
                self.result_box.setVisible(True)
                self.result_image.clear()
                self.result_text.setPlainText("No match found.")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def _find_image_for_person(self, pid):
        for fname in os.listdir(PHOTOS_DIR):
            if fname.startswith(f"{pid}_"):
                return os.path.join(PHOTOS_DIR, fname)
        return None
