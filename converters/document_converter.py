from converters.base import BaseConverter
from typing import Optional
import os
import subprocess
import platform


class DocumentConverter(BaseConverter):
    """Converter for document files."""

    SUPPORTED_FORMATS = ["pdf", "docx", "xlsx", "pptx", "txt", "odt", "rtf"]

    def __init__(self):
        """Initialize document converter."""
        super().__init__()
        self.libreoffice_path = self._find_libreoffice()

    @staticmethod
    def _find_libreoffice() -> str:
        """Find LibreOffice executable path.

        Returns:
            Path to LibreOffice or 'libreoffice' if not found
        """
        if platform.system() == "Windows":
            possible_paths = [
                r"C:\\Program Files\\LibreOffice\\program\\soffice.exe",
                r"C:\\Program Files (x86)\\LibreOffice\\program\\soffice.exe",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    return path
            return "soffice.exe"
        elif platform.system() == "Darwin":
            return "/Applications/LibreOffice.app/Contents/MacOS/soffice"
        return "libreoffice"

    def get_supported_formats(self) -> list:
        """Get supported output formats.

        Returns:
            List of supported format extensions
        """
        return self.SUPPORTED_FORMATS

    def convert(
        self, input_path: str, output_path: str, output_format: str
    ) -> tuple[bool, Optional[str]]:
        """Convert document file.

        Args:
            input_path: Path to input document file
            output_path: Path to output document file
            output_format: Output format (e.g., 'pdf', 'docx')

        Returns:
            Tuple of (success, error_message)
        """
        try:
            self._update_progress(10)

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Format mapping for LibreOffice
            format_map = {
                "pdf": "pdf",
                "docx": "docx",
                "xlsx": "xlsx",
                "pptx": "pptx",
                "txt": "txt",
                "odt": "odt",
                "rtf": "rtf",
            }

            output_format_lower = output_format.lower()
            if output_format_lower not in format_map:
                return False, f"Unsupported document format: {output_format}"

            self._update_progress(30)

            # LibreOffice command for document conversion
            cmd = [
                self.libreoffice_path,
                "--headless",
                "--convert-to",
                format_map[output_format_lower],
                "--outdir",
                os.path.dirname(output_path),
                input_path,
            ]

            self._update_progress(50)

            # Run LibreOffice
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )

            if result.returncode == 0:
                self._update_progress(100)
                return True, None
            else:
                error_msg = result.stderr or "LibreOffice conversion failed"
                return False, f"Document conversion failed: {error_msg}"

        except subprocess.TimeoutExpired:
            return False, "Document conversion timed out"
        except FileNotFoundError:
            return (
                False,
                "LibreOffice not found. Please install LibreOffice to convert documents.",
            )
        except Exception as e:
            return False, f"Document conversion failed: {str(e)}"
