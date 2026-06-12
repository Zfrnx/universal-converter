from converters.base import BaseConverter
from typing import Optional
from PIL import Image
import os


class ImageConverter(BaseConverter):
    """Converter for image files."""

    SUPPORTED_FORMATS = ["png", "jpg", "jpeg", "webp", "bmp", "gif", "tiff", "ico"]

    def get_supported_formats(self) -> list:
        """Get supported output formats.

        Returns:
            List of supported format extensions
        """
        return self.SUPPORTED_FORMATS

    def convert(
        self, input_path: str, output_path: str, output_format: str
    ) -> tuple[bool, Optional[str]]:
        """Convert image file.

        Args:
            input_path: Path to input image file
            output_path: Path to output image file
            output_format: Output format (e.g., 'png', 'jpg')

        Returns:
            Tuple of (success, error_message)
        """
        try:
            self._update_progress(10)

            # Open image
            with Image.open(input_path) as img:
                self._update_progress(40)

                # Convert RGBA to RGB if necessary for formats that don't support alpha
                if (
                    output_format.lower() in ["jpg", "jpeg", "bmp"]
                    and img.mode == "RGBA"
                ):
                    rgb_img = Image.new("RGB", img.size, (255, 255, 255))
                    rgb_img.paste(img, mask=img.split()[3])
                    img = rgb_img

                self._update_progress(70)

                # Save image
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                img.save(output_path, format=output_format.upper())

                self._update_progress(100)
                return True, None

        except Exception as e:
            return False, f"Image conversion failed: {str(e)}"
