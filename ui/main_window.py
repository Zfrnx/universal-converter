from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QProgressBar,
    QFileDialog,
    QMessageBox,
    QListWidget,
    QListWidgetItem,
    QListView,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QDragEnterEvent, QDropEvent
from pathlib import Path
from typing import Optional

from config import Config
from ui.styles import get_theme_stylesheet
from ui.settings_dialog import SettingsDialog
from utils.file_handler import FileHandler
from utils.validators import Validator
from converters import ImageConverter, VideoConverter, DocumentConverter


class ConversionWorker(QThread):
    """Worker thread for file conversion."""

    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(
        self,
        input_file: str,
        output_file: str,
        output_format: str,
        converter,
    ):
        """Initialize worker thread.

        Args:
            input_file: Input file path
            output_file: Output file path
            output_format: Output format
            converter: Converter object
        """
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.output_format = output_format
        self.converter = converter

    def run(self):
        """Run conversion process."""
        self.converter.set_progress_callback(self.progress.emit)
        success, error = self.converter.convert(
            self.input_file, self.output_file, self.output_format
        )
        self.finished.emit(success, error or "")


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        """Initialize main window."""
        super().__init__()
        self.config = Config()
        self.selected_files = []
        self.converters = {
            "Image": ImageConverter(),
            "Video": VideoConverter(),
            "Document": DocumentConverter(),
        }
        self.current_worker: Optional[ConversionWorker] = None
        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        """Initialize user interface."""
        self.setWindowTitle("Universal Converter")
        self.setGeometry(100, 100, 900, 700)
        self.setAcceptDrops(True)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        # Header with title and settings
        header_layout = QHBoxLayout()
        title_label = QLabel("Universal Converter")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        settings_button = QPushButton("⚙️ Settings")
        settings_button.setFixedWidth(120)
        settings_button.clicked.connect(self.open_settings)
        header_layout.addWidget(settings_button)
        main_layout.addLayout(header_layout)

        # File selection area
        file_group_label = QLabel("Step 1: Select Files")
        file_group_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(file_group_label)

        file_layout = QHBoxLayout()
        browse_button = QPushButton("📁 Browse Files")
        browse_button.clicked.connect(self.browse_files)
        clear_button = QPushButton("🗑️ Clear")
        clear_button.clicked.connect(self.clear_files)
        file_layout.addWidget(browse_button)
        file_layout.addWidget(clear_button)
        main_layout.addLayout(file_layout)

        # File list
        self.file_list = QListWidget()
        self.file_list.setMaximumHeight(120)
        main_layout.addWidget(self.file_list)

        # Format selection area
        format_label = QLabel("Step 2: Select Output Format")
        format_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(format_label)

        format_layout = QHBoxLayout()
        format_type_label = QLabel("Format Type:")
        self.format_type_combo = QComboBox()
        self.format_type_combo.addItems(["Image", "Video", "Document"])
        self.format_type_combo.currentTextChanged.connect(self.update_format_options)
        format_layout.addWidget(format_type_label)
        format_layout.addWidget(self.format_type_combo)

        format_name_label = QLabel("Output Format:")
        self.format_combo = QComboBox()
        self.update_format_options()
        format_layout.addWidget(format_name_label)
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch()
        main_layout.addLayout(format_layout)

        # Progress bar
        progress_label = QLabel("Step 3: Convert")
        progress_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Ready")
        main_layout.addWidget(self.status_label)

        # Convert button
        convert_button = QPushButton("▶ Convert")
        convert_button.setFixedHeight(40)
        convert_button.setStyleSheet("font-size: 14px; font-weight: bold;")
        convert_button.clicked.connect(self.start_conversion)
        main_layout.addWidget(convert_button)

        main_layout.addStretch()
        central_widget.setLayout(main_layout)

    def update_format_options(self):
        """Update format options based on selected type."""
        format_type = self.format_type_combo.currentText()
        converter = self.converters.get(format_type)
        if converter:
            self.format_combo.clear()
            self.format_combo.addItems(converter.get_supported_formats())

    def browse_files(self):
        """Browse and select files."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files to Convert",
            str(Path.home()),
            "All Supported Files (*.png *.jpg *.jpeg *.webp *.bmp *.gif *.tiff *.ico *.mp4 *.mkv *.avi *.mov *.flv *.wmv *.webm *.mts *.pdf *.docx *.xlsx *.pptx *.txt *.odt *.rtf)",
        )
        if files:
            self.selected_files.extend(files)
            self.update_file_list()

    def clear_files(self):
        """Clear selected files."""
        self.selected_files.clear()
        self.file_list.clear()
        self.status_label.setText("Ready")

    def update_file_list(self):
        """Update file list display."""
        self.file_list.clear()
        for file_path in self.selected_files:
            item = QListWidgetItem(Path(file_path).name)
            self.file_list.addItem(item)

    def start_conversion(self):
        """Start file conversion process."""
        if not self.selected_files:
            QMessageBox.warning(self, "Warning", "Please select files to convert.")
            return

        # For now, convert the first file
        input_file = self.selected_files[0]
        output_format = self.format_combo.currentText()

        # Validate conversion
        valid, error = Validator.validate_conversion(input_file, output_format)
        if not valid:
            QMessageBox.critical(self, "Error", f"Conversion error: {error}")
            return

        # Get output path
        output_dir = self.config.get_output_directory()
        output_file = FileHandler.get_output_path(input_file, output_dir, output_format)
        output_file = FileHandler.ensure_unique_filename(output_file)

        # Get appropriate converter
        file_category = FileHandler.get_file_category(input_file)
        converter = self.converters.get(
            "Image" if file_category == "image" else ("Video" if file_category == "video" else "Document")
        )

        if not converter:
            QMessageBox.critical(self, "Error", "No suitable converter found.")
            return

        # Create and start worker thread
        self.current_worker = ConversionWorker(
            input_file, output_file, output_format, converter
        )
        self.current_worker.progress.connect(self.update_progress)
        self.current_worker.finished.connect(self.conversion_finished)
        self.progress_bar.setValue(0)
        self.status_label.setText(f"Converting: {Path(input_file).name}...")
        self.current_worker.start()

    def update_progress(self, value: int):
        """Update progress bar.

        Args:
            value: Progress percentage
        """
        self.progress_bar.setValue(value)

    def conversion_finished(self, success: bool, error: str):
        """Handle conversion completion.

        Args:
            success: Whether conversion was successful
            error: Error message if conversion failed
        """
        if success:
            self.status_label.setText("✓ Conversion completed successfully!")
            self.progress_bar.setValue(100)
            # Remove converted file from list
            if self.selected_files:
                self.selected_files.pop(0)
                self.update_file_list()
                if self.selected_files:
                    self.status_label.setText(
                        f"Ready to convert {len(self.selected_files)} more file(s)"
                    )
                else:
                    self.status_label.setText("All files converted!")
        else:
            self.status_label.setText(f"✗ Conversion failed: {error}")
            QMessageBox.critical(self, "Conversion Error", f"Error: {error}")

    def open_settings(self):
        """Open settings dialog."""
        dialog = SettingsDialog(self.config, self)
        dialog.exec()
        self.apply_theme()

    def apply_theme(self):
        """Apply current theme to application."""
        theme = self.config.get_theme()
        stylesheet = get_theme_stylesheet(theme)
        self.setStyleSheet(stylesheet)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event.

        Args:
            event: Drag event
        """
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        """Handle drop event.

        Args:
            event: Drop event
        """
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if Path(file_path).is_file():
                self.selected_files.append(file_path)
        self.update_file_list()
