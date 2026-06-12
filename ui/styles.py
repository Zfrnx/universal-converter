"""Application styles and themes."""

LIGHT_THEME = """
    QMainWindow {
        background-color: #FFFFFF;
        color: #000000;
    }
    QMenuBar {
        background-color: #F5F5F5;
        color: #000000;
        border-bottom: 1px solid #E0E0E0;
    }
    QMenuBar::item:selected {
        background-color: #E0E0E0;
    }
    QMenu {
        background-color: #F5F5F5;
        color: #000000;
        border: 1px solid #E0E0E0;
    }
    QMenu::item:selected {
        background-color: #E0E0E0;
    }
    QPushButton {
        background-color: #007ACC;
        color: #FFFFFF;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #005A9E;
    }
    QPushButton:pressed {
        background-color: #004578;
    }
    QLineEdit, QTextEdit {
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #D0D0D0;
        border-radius: 4px;
        padding: 6px;
    }
    QComboBox {
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #D0D0D0;
        border-radius: 4px;
        padding: 6px;
    }
    QLabel {
        color: #000000;
    }
    QProgressBar {
        background-color: #E0E0E0;
        border: 1px solid #D0D0D0;
        border-radius: 4px;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #007ACC;
    }
    QGroupBox {
        color: #000000;
        border: 1px solid #D0D0D0;
        border-radius: 4px;
        margin-top: 1ex;
        padding-top: 10px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 3px 0 3px;
    }
"""

DARK_THEME = """
    QMainWindow {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    QMenuBar {
        background-color: #2D2D2D;
        color: #FFFFFF;
        border-bottom: 1px solid #3E3E3E;
    }
    QMenuBar::item:selected {
        background-color: #3E3E3E;
    }
    QMenu {
        background-color: #2D2D2D;
        color: #FFFFFF;
        border: 1px solid #3E3E3E;
    }
    QMenu::item:selected {
        background-color: #3E3E3E;
    }
    QPushButton {
        background-color: #0E639C;
        color: #FFFFFF;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #1177BB;
    }
    QPushButton:pressed {
        background-color: #0A3F5E;
    }
    QLineEdit, QTextEdit {
        background-color: #3E3E3E;
        color: #FFFFFF;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 6px;
    }
    QComboBox {
        background-color: #3E3E3E;
        color: #FFFFFF;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 6px;
    }
    QLabel {
        color: #FFFFFF;
    }
    QProgressBar {
        background-color: #3E3E3E;
        border: 1px solid #555555;
        border-radius: 4px;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #0E639C;
    }
    QGroupBox {
        color: #FFFFFF;
        border: 1px solid #555555;
        border-radius: 4px;
        margin-top: 1ex;
        padding-top: 10px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 3px 0 3px;
    }
"""


def get_theme_stylesheet(theme: str) -> str:
    """Get stylesheet for specified theme.

    Args:
        theme: Theme name ('light' or 'dark')

    Returns:
        Stylesheet string
    """
    return DARK_THEME if theme == "dark" else LIGHT_THEME
