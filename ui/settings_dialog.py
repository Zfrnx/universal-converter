from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QFileDialog,
    QGroupBox,
)
from PyQt6.QtCore import Qt
from config import Config
from ui.styles import get_theme_stylesheet


class SettingsDialog(QDialog):
    """Settings dialog for application configuration."""

    def __init__(self, config: Config, parent=None):
        """Initialize settings dialog.

        Args:
            config: Configuration object
            parent: Parent widget
        """
        super().__init__(parent)
        self.config = config
        self.init_ui()

    def init_ui(self):
        """Initialize user interface."""
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 500, 300)
        self.setModal(True)

        layout = QVBoxLayout()

        # Output Directory Group
        output_group = QGroupBox("Output Directory")
        output_layout = QHBoxLayout()

        output_label = QLabel("Save location:")
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setText(self.config.get_output_directory())
        self.output_path_edit.setReadOnly(True)

        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_output_directory)

        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_path_edit)
        output_layout.addWidget(browse_button)
        output_group.setLayout(output_layout)

        # Theme Group
        theme_group = QGroupBox("Appearance")
        theme_layout = QHBoxLayout()

        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        current_theme = self.config.get_theme()
        self.theme_combo.setCurrentText("Dark" if current_theme == "dark" else "Light")
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)

        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        theme_group.setLayout(theme_layout)

        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")

        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        # Add all groups to main layout
        layout.addWidget(output_group)
        layout.addWidget(theme_group)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.apply_theme()

    def browse_output_directory(self):
        """Browse for output directory."""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            self.output_path_edit.text(),
        )
        if directory:
            if self.config.set_output_directory(directory):
                self.output_path_edit.setText(directory)

    def on_theme_changed(self, theme_name: str):
        """Handle theme change.

        Args:
            theme_name: Selected theme name
        """
        theme = "dark" if theme_name == "Dark" else "light"
        self.config.set_theme(theme)
        self.apply_theme()

    def apply_theme(self):
        """Apply current theme to dialog."""
        theme = self.config.get_theme()
        stylesheet = get_theme_stylesheet(theme)
        self.setStyleSheet(stylesheet)

    def accept(self):
        """Accept changes and close dialog."""
        super().accept()
