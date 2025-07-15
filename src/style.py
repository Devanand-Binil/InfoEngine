def setup_stylesheet(app):
    """Apply a professional, scalable, subtly espionage-inspired stylesheet."""

    stylesheet = """
    * {
        font-family: 'Segoe UI', 'SF Pro Display', 'Roboto', 'Helvetica Neue', sans-serif;
        font-size: 14px;
        color: #1D3557;
    }

    QWidget {
        background-color: #F8F9FA;
    }

    QMainWindow {
        background-color: #FFFFFF;
    }

    QLabel {
        color: #1D3557;
        font-weight: 500;
        padding: 4px;
    }

    QLabel.heading1 {
        font-size: 22px;
        font-weight: 600;
        padding: 6px 0;
        color: #1D3557;
        border-bottom: 2px solid #A8DADC;
    }

    QLabel.heading2 {
        font-size: 16px;
        font-weight: 600;
        color: #E63946;
        margin-bottom: 4px;
    }

    QPushButton {
        padding: 8px 16px;
        background-color: #1D3557;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 500;
    }

    QPushButton:hover {
        background-color: #457B9D;
    }

    QPushButton:pressed {
        background-color: #E63946;
    }

    QPushButton:disabled {
        background-color: #CED4DA;
        color: #6C757D;
    }

    QLineEdit, QTextEdit, QPlainTextEdit {
        background-color: #FFFFFF;
        border: 1px solid #CED4DA;
        border-radius: 4px;
        padding: 6px;
        color: #1D3557;
    }

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border: 1px solid #457B9D;
        outline: none;
    }

    QTabWidget::pane {
        border: 1px solid #DEE2E6;
        border-radius: 6px;
        top: -1px;
        background: #FFFFFF;
    }

    QTabBar::tab {
        background-color: #E9ECEF;
        color: #1D3557;
        padding: 8px 16px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        margin-right: 2px;
        font-weight: 500;
    }

    QTabBar::tab:selected {
        background-color: #FFFFFF;
        border: 1px solid #DEE2E6;
        border-bottom: none;
    }

    QTabBar::tab:hover {
        background-color: #DDEAF2;
    }

    QStatusBar {
        background-color: #F1F3F5;
        color: #495057;
        border-top: 1px solid #DEE2E6;
    }

    QSplitter::handle {
        background-color: #A8DADC;
    }

    QScrollBar:vertical, QScrollBar:horizontal {
        background: #F1F3F5;
        width: 10px;
    }

    QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
        background: #ADB5BD;
        min-height: 20px;
        border-radius: 4px;
    }

    QToolTip {
        background-color: #FFFFFF;
        color: #1D3557;
        border: 1px solid #CED4DA;
        padding: 4px;
    }

    QProgressBar {
        border: 1px solid #CED4DA;
        border-radius: 4px;
        background-color: #E9ECEF;
        text-align: center;
    }

    QProgressBar::chunk {
        background-color: #457B9D;
        border-radius: 4px;
    }

    QTableWidget {
        background-color: #FFFFFF;
        border: 1px solid #DEE2E6;
        border-radius: 6px;
        gridline-color: #DEE2E6;
    }

    QHeaderView::section {
        background-color: #1D3557;
        color: white;
        font-weight: bold;
        padding: 6px;
        border: none;
    }
    """

    app.setStyleSheet(stylesheet)
