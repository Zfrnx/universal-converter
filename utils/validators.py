import os
from typing import List, Optional
from utils.file_handler import FileHandler


class Validator:
    """Utility class for validation operations."""

    @staticmethod
    def validate_file_exists(file_path: str) -> bool:
        """Validate that file exists.

        Args:
            file_path: File path

        Returns:
            True if file exists, False otherwise
        """
        return os.path.isfile(file_path)

    @staticmethod
    def validate_file_readable(file_path: str) -> bool:
        """Validate that file is readable.

        Args:
            file_path: File path

        Returns:
            True if file is readable, False otherwise
        """
        return os.access(file_path, os.R_OK)

    @staticmethod
    def validate_directory_writable(directory: str) -> bool:
        """Validate that directory is writable.

        Args:
            directory: Directory path

        Returns:
            True if directory is writable, False otherwise
        """
        return os.access(directory, os.W_OK)

    @staticmethod
    def validate_conversion(
        input_file: str, output_format: str
    ) -> tuple[bool, Optional[str]]:
        """Validate conversion parameters.

        Args:
            input_file: Input file path
            output_format: Desired output format

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not Validator.validate_file_exists(input_file):
            return False, "Input file does not exist"

        if not Validator.validate_file_readable(input_file):
            return False, "Input file is not readable"

        if not FileHandler.is_supported(input_file):
            return False, f"File format not supported"

        input_category = FileHandler.get_file_category(input_file)
        output_format_lower = output_format.lower().lstrip(".")

        if output_format_lower not in FileHandler.SUPPORTED_FORMATS.get(
            input_category, []
        ):
            return False, f"Cannot convert to {output_format} format"

        return True, None

    @staticmethod
    def validate_batch_files(file_list: List[str]) -> tuple[List[str], List[str]]:
        """Validate batch file list.

        Args:
            file_list: List of file paths

        Returns:
            Tuple of (valid_files, invalid_files)
        """
        valid_files = []
        invalid_files = []

        for file_path in file_list:
            if (
                Validator.validate_file_exists(file_path)
                and Validator.validate_file_readable(file_path)
                and FileHandler.is_supported(file_path)
            ):
                valid_files.append(file_path)
            else:
                invalid_files.append(file_path)

        return valid_files, invalid_files
