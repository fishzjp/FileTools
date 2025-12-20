[English](English_README.md) | [简体中文](../README.md)

[![GitHub stars](https://img.shields.io/github/stars/fishzjp/FileTools)](https://github.com/fishzjp/FileTools)
[![GitHub forks](https://img.shields.io/github/forks/fishzjp/FileTools)](https://github.com/fishzjp/FileTools)

---

# 📁 File Size Generator Tool

A file generation tool built with **Gradio** for quickly generating files of specified sizes and monitoring disk space usage in real-time. Suitable for software development, system testing, and scenarios that need to simulate full disk conditions.

## ✨ Features

1. **Modern Web Interface**: Built with Gradio for an intuitive and user-friendly Web UI, supporting cross-platform access
2. **Fast File Generation**: Efficient chunk-based writing algorithm for quick generation of files of any size (KB/MB/GB/TB)
3. **Real-time Disk Monitoring**: Real-time display of disk usage with support for multiple unit switching
4. **Smart Error Handling**: Comprehensive input validation and error messages, including disk space checking
5. **Cross-platform Support**: Supports Windows, macOS, and Linux systems
6. **Comprehensive Test Coverage**: Unit tests using pytest to ensure code quality
7. **Logging System**: Complete logging system for troubleshooting

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
# Install dependencies (from pyproject.toml)
pip install -e .

# Or install packages directly
pip install psutil>=7.1.3 gradio>=4.0.0

# Run the application
python main.py
```

For detailed installation instructions, see [Installation Guide](docs/installation.md).

### Usage

1. After starting the application, the browser will automatically open (default address: `http://localhost:7860`)
2. In the "File Generation Settings" area:
   - Enter the save path (e.g., `/Users/username/Downloads`)
   - Enter the file name (e.g., `test_file.bin`)
   - Enter the file size and select the unit (KB/MB/GB/TB)
3. Click the "Generate File" button
4. View disk usage in real-time in the "Disk Space Monitoring" area

For detailed usage instructions, see [Usage Guide](docs/usage.md).

## 📁 Project Structure

```
FileTools/
├── main.py                 # Main entry file
├── pyproject.toml          # Project configuration and dependency management
├── LICENSE                 # MIT License
├── docs/                   # Documentation directory
│   ├── CHANGELOG.md        # Version changelog
│   ├── English_README.md   # English README
│   ├── contributing.md     # Contributing guide
│   ├── development.md      # Development guide
│   ├── installation.md     # Installation guide
│   ├── usage.md            # Usage guide
│   ├── testing.md          # Testing documentation
│   ├── logging.md          # Logging documentation
│   └── faq.md              # FAQ
├── src/                    # Source code directory
│   └── filetools/          # Main package
│       ├── __init__.py
│       ├── config/         # Configuration module
│       │   ├── __init__.py
│       │   ├── constants.py # Constants definition
│       │   └── logger.py   # Logging configuration
│       ├── models/          # Business logic module
│       │   ├── __init__.py
│       │   ├── file_generator.py  # File generation logic
│       │   ├── disk_monitor.py    # Disk monitoring logic
│       │   └── disk_usage.py      # Disk usage data model
│       └── ui/              # UI module
│           ├── __init__.py
│           └── interface.py # Gradio interface components
├── tests/                  # Test module
│   ├── __init__.py
│   ├── test_constants.py
│   ├── test_disk_monitor.py
│   ├── test_file_generator.py
│   ├── test_file_generator_core.py
│   ├── test_ui_functions.py
│   └── test_ui_validation.py
├── docs/                   # Documentation directory
│   ├── installation.md    # Installation guide
│   ├── usage.md           # Usage guide
│   ├── development.md     # Development guide
│   ├── testing.md         # Testing documentation
│   ├── logging.md         # Logging documentation
│   ├── faq.md             # FAQ
│   └── contributing.md    # Contributing guide
├── assets/                 # Assets directory
│   └── 扫码_搜索联合传播样式-白色版.png
└── .github/                # GitHub configuration
    └── workflows/
        └── ci.yml          # CI workflow
```

For complete project structure details, see [Development Guide](docs/development.md).

## 🔧 Technical Architecture

- **Frontend Framework**: Gradio (Python Web UI framework)
- **System Monitoring**: psutil (cross-platform system monitoring library)
- **File Operations**: Python standard library `pathlib`, `io`
- **Testing Framework**: pytest
- **Architecture Pattern**: Modular design with clear separation of concerns

## 💡 Core Features

### File Generation

- Supports KB, MB, GB, TB units
- Uses chunk-based writing algorithm (100MB chunks) for fast generation
- Automatic file size and disk space validation
- Comprehensive error handling and messages
- Supports progress callback for real-time generation progress

### Disk Monitoring

- Real-time display of all disk partition usage
- Intelligent filtering of system partitions (macOS/Windows)
- Support for multiple display unit switching (KB/MB/GB/TB)
- Shows usage rate, used space, available space, and total space
- Automatic refresh and manual refresh modes

## 📚 Documentation

- [Installation Guide](docs/installation.md) - Detailed installation instructions and environment setup
- [Usage Guide](docs/usage.md) - Feature usage instructions and examples
- [Development Guide](docs/development.md) - Development environment setup and code standards
- [Testing Documentation](docs/testing.md) - Test execution and writing guidelines
- [Logging Documentation](docs/logging.md) - Logging configuration and viewing methods
- [FAQ](docs/faq.md) - Frequently asked questions and troubleshooting
- [Contributing Guide](docs/contributing.md) - How to contribute to the project

## 🧪 Testing

The project uses `pytest` for unit testing. Run tests:

```bash
# Run tests using uv (recommended)
uv run pytest

# Run tests with coverage
uv run pytest --cov=models --cov=ui --cov=config
```

For detailed testing instructions, see [Testing Documentation](docs/testing.md).

## ❓ Frequently Asked Questions

Having issues? Please check the [FAQ Documentation](docs/faq.md) first.

## 🤝 Contributing

Issues and Pull Requests are welcome! For detailed instructions, see [Contributing Guide](docs/contributing.md).

- 📝 [Submit an Issue](https://github.com/fishzjp/FileTools/issues)
- 🔀 [Submit a Pull Request](https://github.com/fishzjp/FileTools/pulls)
- 📦 [Repository](https://github.com/fishzjp/FileTools)

## 📄 License

This project is licensed under the MIT License.

---

Hope this tool helps you! If you have any questions or suggestions, please feel free to provide feedback.
