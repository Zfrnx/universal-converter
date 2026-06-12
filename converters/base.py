from abc import ABC, abstractmethod
from typing import Optional


class BaseConverter(ABC):
    """Base converter class for all file type converters."""

    def __init__(self):
        """Initialize converter."""
        self.progress_callback = None

    def set_progress_callback(self, callback) -> None:
        """Set callback for progress updates.

        Args:
            callback: Callback function that receives progress percentage
        """
        self.progress_callback = callback

    def _update_progress(self, percentage: int) -> None:
        """Update progress.

        Args:
            percentage: Progress percentage (0-100)
        """
        if self.progress_callback:
            self.progress_callback(percentage)

    @abstractmethod
    def get_supported_formats(self) -> list:
        """Get supported output formats.

        Returns:
            List of supported format extensions
        """
        pass

    @abstractmethod
    def convert(
        self, input_path: str, output_path: str, output_format: str
    ) -> tuple[bool, Optional[str]]:
        """Convert file.

        Args:
            input_path: Path to input file
            output_path: Path to output file
            output_format: Output format

        Returns:
            Tuple of (success, error_message)
        """
        pass
