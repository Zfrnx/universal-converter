import os
import shutil
from pathlib import Path
from typing import Optional


class FileHandler:
    """Utility class for file operations."""

    SUPPORTED_FORMATS = {
        "image": ["png", "jpg", "jpeg", "webp", "bmp", "gif", "tiff", "ico"],
        "video": ["mp4", "mkv", "avi", "mov", "flv", "wmv", "webm", "mts"],
        "document": ["pdf", "docx", "xlsx", "pptx", "txt", "odt", "rtf"],
    }

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """Get file extension.

        Args:
            file_path: Path to file

        Returns:
            File extension without dot
        """
        return Path(file_path).suffix.lower().lstrip(".")

    @staticmethod
    def get_file_category(file_path: str) -> Optional[str]:
        """Get file category based on extension.

        Args:
            file_path: Path to file

        Returns:
            Category ('image', 'video', 'document') or None
        """
        ext = FileHandler.get_file_extension(file_path)
        for category, extensions in FileHandler.SUPPORTED_FORMATS.items():
            if ext in extensions:
                return category
        return None

    @staticmethod
    def is_supported(file_path: str) -> bool:
        """Check if file format is supported.

        Args:
            file_path: Path to file

        Returns:
            True if supported, False otherwise
        """
        return FileHandler.get_file_category(file_path) is not None

    @staticmethod
    def get_output_path(
        input_path: str, output_dir: str, new_extension: str
    ) -> str:
        """Generate output file path.

        Args:
            input_path: Input file path
            output_dir: Output directory
            new_extension: New file extension (without dot)

        Returns:
            Output file path
        """
        file_name = Path(input_path).stem
        return os.path.join(output_dir, f"{file_name}.{new_extension}")

    @staticmethod
    def ensure_unique_filename(file_path: str) -> str:
        """Ensure filename is unique by adding counter if needed.

        Args:
            file_path: File path

        Returns:
            Unique file path
        """
        if not os.path.exists(file_path):
            return file_path

        path = Path(file_path)
        counter = 1
        while True:
            new_name = f"{path.stem}_{counter}{path.suffix}"
            new_path = path.parent / new_name
            if not os.path.exists(new_path):
                return str(new_path)
            counter += 1

    @staticmethod
    def copy_file(source: str, destination: str) -> bool:
        """Copy file from source to destination.

        Args:
            source: Source file path
            destination: Destination file path

        Returns:
            True if successful, False otherwise
        """
        try:
            shutil.copy2(source, destination)
            return True
        except (OSError, IOError):
            return False

    @staticmethod
    def delete_file(file_path: str) -> bool:
        """Delete file.

        Args:
            file_path: File path

        Returns:
            True if successful, False otherwise
        """
        try:
            os.remove(file_path)
            return True
        except (OSError, FileNotFoundError):
            return False
