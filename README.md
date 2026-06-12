# Universal Converter

A modern, user-friendly desktop application for converting files across multiple formats including images, videos, and documents.

## Features

✨ **Multi-Format Support**
- **Images**: PNG, JPG, JPEG, WEBP, BMP, GIF, TIFF, ICO
- **Videos**: MP4, MKV, AVI, MOV, FLV, WMV, WEBM, MTS
- **Documents**: PDF, DOCX, XLSX, PPTX, TXT, ODT, RTF

🎨 **User Interface**
- Clean, intuitive GUI built with PyQt6
- Drag-and-drop file support
- Batch conversion capabilities
- Real-time conversion progress

⚙️ **Settings & Customization**
- Toggle settings menu
- Custom output directory configuration
- Dark/Light theme support
- Persistent configuration storage

🔧 **Technical Features**
- Modular architecture with separate utility modules
- Efficient file processing
- Cross-platform compatibility (Windows, macOS, Linux)

## Installation

### Requirements
- Python 3.8+
- FFmpeg (for video conversion)
- ImageMagick (for image conversion)
- LibreOffice (for document conversion)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Zfrnx/universal-converter.git
cd universal-converter
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install system dependencies:

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg imagemagick libreoffice
```

**macOS:**
```bash
brew install ffmpeg imagemagick libreoffice
```

**Windows:**
- Download and install FFmpeg from https://ffmpeg.org/download.html
- Download and install ImageMagick from https://imagemagick.org/script/download.php
- Download and install LibreOffice from https://www.libreoffice.org/download/

## Usage

Run the application:
```bash
python main.py
```

### Basic Workflow
1. Launch the application
2. Select or drag-drop files to convert
3. Choose output format
4. Configure conversion options (if available)
5. Click "Convert"
6. Access converted files in your configured output directory

### Settings
- Click the **Settings** (⚙️) icon in the top-right corner
- Configure output directory
- Toggle between Dark/Light themes
- Changes are saved automatically

## Project Structure

```
universal-converter/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── config.json            # User settings (auto-generated)
├── config.py              # Configuration management
├── ui/
│   ├── main_window.py     # Main application window
│   ├── settings_dialog.py # Settings interface
│   └── styles.py          # Theme and styling
├── converters/
│   ├── __init__.py
│   ├── base.py            # Base converter class
│   ├── image_converter.py # Image conversion utilities
│   ├── video_converter.py # Video conversion utilities
│   └── document_converter.py # Document conversion utilities
└── utils/
    ├── __init__.py
    ├── file_handler.py    # File I/O operations
    └── validators.py      # Format validation
```

## Dependencies

- **PyQt6**: GUI framework
- **Pillow**: Image processing
- **moviepy**: Video processing
- **python-pptx**: PowerPoint handling
- **python-docx**: Word document handling
- **openpyxl**: Excel handling
- **pypdf**: PDF handling

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, feature requests, or questions, please open an issue on GitHub.
