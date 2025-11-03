
[English](English_README.md) | [简体中文](README.md)
---

# 📁 File Size Generator Tool

A file generation tool built with **Gradio** for quickly generating files of specified sizes and monitoring disk space usage in real-time. Suitable for software development, system testing, and scenarios that need to simulate full disk conditions.

## ✨ Features

1. **Modern Web Interface**: Built with Gradio for an intuitive and user-friendly Web UI, supporting cross-platform access
2. **Fast File Generation**: Efficient chunk-based writing algorithm for quick generation of files of any size (KB/MB/GB/TB)
3. **Real-time Disk Monitoring**: Real-time display of disk usage with support for multiple unit switching
4. **Smart Error Handling**: Comprehensive input validation and error messages, including disk space checking
5. **Cross-platform Support**: Supports Windows, macOS, and Linux systems

## 🚀 Quick Start

### Requirements

- Python >= 3.11
- Dependencies: `psutil`, `gradio`

### Installation

Using `uv` package manager (recommended):

```bash
# Install dependencies
uv sync

# Run the application
uv run python main.py
```

Or using traditional method:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Usage

1. After starting the application, the browser will automatically open (default address: `http://localhost:7860`)
2. In the "File Generation Settings" area:
   - Enter the save path (e.g., `/Users/username/Downloads`)
   - Enter the file name (e.g., `test_file.bin`)
   - Enter the file size and select the unit (KB/MB/GB/TB)
3. Click the "Generate File" button
4. View disk usage in real-time in the "Disk Space Monitoring" area
5. Switch display units or manually refresh disk information

## 📁 Project Structure

```
FileTools/
├── main.py                 # Main entry file
├── config/                 # Configuration module
│   ├── constants.py       # Constants definition
│   └── __init__.py
├── models/                 # Business logic module
│   ├── file_generator.py  # File generation logic
│   ├── disk_monitor.py    # Disk monitoring logic
│   └── __init__.py
├── ui/                     # UI module
│   ├── interface.py       # Gradio interface components
│   └── __init__.py
└── utils/                  # Utility functions module
    ├── disk.py            # Disk utility functions
    └── __init__.py
```

## 🔧 Technical Architecture

- **Frontend Framework**: Gradio (Python Web UI framework)
- **System Monitoring**: psutil (cross-platform system monitoring library)
- **File Operations**: Python standard library `pathlib`, `io`
- **Architecture Pattern**: Modular design with clear separation of concerns

## 💡 Core Features

### File Generation

- Supports KB, MB, GB, TB units
- Uses chunk-based writing algorithm (100MB chunks) for fast generation
- Automatic file size and disk space validation
- Comprehensive error handling and messages

### Disk Monitoring

- Real-time display of all disk partition usage
- Intelligent filtering of system partitions (macOS/Windows)
- Support for multiple display unit switching
- Shows usage rate, used space, available space, and total space

## 📝 Development Notes

### Code Optimization Highlights

1. **Modular Architecture**: Clear separation of UI, business logic, and utility functions
2. **Error Handling**: Comprehensive exception handling with user-friendly error messages
3. **Type Annotations**: Complete type hints for improved code maintainability
4. **Documentation**: Detailed function documentation for easy understanding and maintenance

### Runtime Configuration

Default configuration:
- Server address: `0.0.0.0`
- Port: `7860`
- Share link: Disabled

You can modify startup parameters in `main.py`.

## 📦 Packaging (Optional)

If you need to package as a standalone application, you can use PyInstaller:

```bash
# Package with upx compression (requires upx installation)
pyinstaller --onefile --noconsole --upx-dir=path/to/upx main.py

# Package without upx compression
pyinstaller --onefile --noconsole main.py
```

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

This project is licensed under the MIT License.

---

Hope this tool helps you! If you have any questions or suggestions, please feel free to provide feedback.
