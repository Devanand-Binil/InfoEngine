# main.py

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFontDatabase, QFont

from src.splash_screen import SplashScreen
from src.main_window import MainWindow
from src.style import setup_stylesheet


def load_custom_fonts(fonts_dir: str):
    """
    Loads all .ttf fonts from the specified fonts directory.
    Logs warnings or errors if fonts cannot be loaded.
    """
    if not os.path.exists(fonts_dir):
        print(f"[⚠️ Warning] Font directory not found: {fonts_dir}")
        return

    for font_file in os.listdir(fonts_dir):
        if font_file.lower().endswith('.ttf'):
            font_path = os.path.join(fonts_dir, font_file)
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id == -1:
                print(f"[❌ Error] Failed to load font: {font_file}")
            else:
                print(f"[✅ Loaded Font] {font_file}")


def main():
    """
    Entry point for the Information Engine desktop application.
    Sets up theme, fonts, splash screen, and launches the main interface.
    """
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Information Engine")

        # Apply global stylesheet (light/dark, custom colors, etc.)
        setup_stylesheet(app)

        # Load custom fonts (optional)
        fonts_dir = os.path.join(os.path.dirname(__file__), "assets", "fonts")
        load_custom_fonts(fonts_dir)

        # Set default application font
        default_font = QFont("SF Pro Display", 10)
        app.setFont(default_font)

        # Show splash screen
        splash = SplashScreen()
        splash.show()

        # Load the main application window
        main_window = MainWindow()

        # Delay to simulate loading time and transition
        QTimer.singleShot(2500, lambda: splash.finish(main_window) or main_window.show())

        sys.exit(app.exec_())

    except Exception as e:
        print(f"[🔥 Fatal Error] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
