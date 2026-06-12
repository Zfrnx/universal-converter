import json
import os
from pathlib import Path
from typing import Any, Dict


class Config:
    """Configuration manager for the Universal Converter application."""

    DEFAULT_CONFIG = {
        "output_directory": str(Path.home() / "Downloads" / "Converted"),
        "theme": "light",
        "window_width": 900,
        "window_height": 700,
    }

    def __init__(self, config_path: str = "config.json"):
        """Initialize configuration manager.

        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config: Dict[str, Any] = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default.

        Returns:
            Configuration dictionary
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return {**self.DEFAULT_CONFIG, **config}
            except (json.JSONDecodeError, IOError):
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()

    def save_config(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"Error saving configuration: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value.

        Args:
            key: Configuration key
            value: Value to set
        """
        self.config[key] = value
        self.save_config()

    def get_output_directory(self) -> str:
        """Get output directory, creating it if it doesn't exist.

        Returns:
            Output directory path
        """
        output_dir = self.get("output_directory")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        return output_dir

    def set_output_directory(self, path: str) -> bool:
        """Set output directory.

        Args:
            path: Directory path

        Returns:
            True if successful, False otherwise
        """
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            self.set("output_directory", path)
            return True
        except (OSError, PermissionError):
            return False

    def get_theme(self) -> str:
        """Get current theme.

        Returns:
            Theme name ('light' or 'dark')
        """
        return self.get("theme", "light")

    def set_theme(self, theme: str) -> None:
        """Set theme.

        Args:
            theme: Theme name ('light' or 'dark')
        """
        if theme in ["light", "dark"]:
            self.set("theme", theme)
