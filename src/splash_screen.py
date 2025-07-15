# bolt/src/splash_screen.py

from PyQt5.QtWidgets import QSplashScreen, QProgressBar, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor, QPainter, QFont


class SplashScreen(QSplashScreen):
    finished = pyqtSignal()  # Emitted when loading is complete

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._init_ui()
        self._init_progress_bar()
        self._init_timer()

    def _init_ui(self):
        """Draw splash background and text."""
        size = QSize(600, 400)
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Rounded background with shadow color
        painter.setBrush(QColor("#1D3557"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, size.width(), size.height(), 20, 20)

        # Title
        title_font = QFont("SF Pro Display", 36, QFont.Bold)
        if not title_font.exactMatch():
            title_font = QFont("Arial", 36, QFont.Bold)  # Fallback

        painter.setFont(title_font)
        painter.setPen(QColor("#F1FAEE"))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "Information Engine")

        # Tagline
        tagline_font = QFont("SF Pro Display", 14)
        painter.setFont(tagline_font)
        painter.setPen(QColor("#A8DADC"))
        painter.drawText(pixmap.rect().adjusted(0, 90, 0, 0),
                         Qt.AlignHCenter | Qt.AlignTop,
                         "Intelligent Search & Recognition Suite")

        painter.end()
        self.setPixmap(pixmap)

        # Optional shadow effect
        self._add_shadow()

    def _add_shadow(self):
        """Applies drop shadow for modern floating effect."""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(shadow)

    def _init_progress_bar(self):
        """Sets up styled progress bar."""
        size = self.pixmap().size()
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(50, size.height() - 40, size.width() - 100, 8)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)

        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #457B9D;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #E63946;
                border-radius: 4px;
            }
        """)

    def _init_timer(self):
        """Simulates loading progress."""
        self.progress = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_progress)
        self.timer.start(25)

    def _update_progress(self):
        """Updates progress bar every tick."""
        self.progress += 1
        self.progress_bar.setValue(self.progress)

        if self.progress >= 100:
            self.timer.stop()
            self.finished.emit()

    def mousePressEvent(self, event):
        """Prevent user interaction."""
        pass
