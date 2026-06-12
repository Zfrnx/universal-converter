from converters.base import BaseConverter
from typing import Optional
import os
import subprocess
import platform


class VideoConverter(BaseConverter):
    """Converter for video files."""

    SUPPORTED_FORMATS = ["mp4", "mkv", "avi", "mov", "flv", "wmv", "webm", "mts"]

    def __init__(self):
        """Initialize video converter."""
        super().__init__()
        self.ffmpeg_path = self._find_ffmpeg()

    @staticmethod
    def _find_ffmpeg() -> str:
        """Find FFmpeg executable path.

        Returns:
            Path to FFmpeg or 'ffmpeg' if not found
        """
        if platform.system() == "Windows":
            possible_paths = [
                r"C:\\ffmpeg\\bin\\ffmpeg.exe",
                r"C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    return path
        return "ffmpeg"

    def get_supported_formats(self) -> list:
        """Get supported output formats.

        Returns:
            List of supported format extensions
        """
        return self.SUPPORTED_FORMATS

    def convert(
        self, input_path: str, output_path: str, output_format: str
    ) -> tuple[bool, Optional[str]]:
        """Convert video file.

        Args:
            input_path: Path to input video file
            output_path: Path to output video file
            output_format: Output format (e.g., 'mp4', 'mkv')

        Returns:
            Tuple of (success, error_message)
        """
        try:
            self._update_progress(10)

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # FFmpeg command for video conversion
            cmd = [
                self.ffmpeg_path,
                "-i",
                input_path,
                "-c:v",
                "libx264",  # Video codec
                "-c:a",
                "aac",  # Audio codec
                "-y",  # Overwrite output file
                output_path,
            ]

            self._update_progress(30)

            # Run FFmpeg
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600,  # 1 hour timeout
            )

            if result.returncode == 0:
                self._update_progress(100)
                return True, None
            else:
                error_msg = result.stderr or "FFmpeg conversion failed"
                return False, f"Video conversion failed: {error_msg}"

        except subprocess.TimeoutExpired:
            return False, "Video conversion timed out"
        except FileNotFoundError:
            return (
                False,
                "FFmpeg not found. Please install FFmpeg to convert videos.",
            )
        except Exception as e:
            return False, f"Video conversion failed: {str(e)}"
