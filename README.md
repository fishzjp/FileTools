[English](docs/English_README.md) | [简体中文](README.md)

[![GitHub stars](https://img.shields.io/github/stars/fishzjp/FileTools)](https://github.com/fishzjp/FileTools)
[![GitHub forks](https://img.shields.io/github/forks/fishzjp/FileTools)](https://github.com/fishzjp/FileTools)

---

# 📁 文件大小生成工具

一个基于 **Gradio** 的文件生成工具，用于快速生成指定大小的文件，并实时监控磁盘空间使用情况。适用于软件开发、系统测试等需要模拟磁盘空间满的场景。

## ✨ 项目特点

1. **现代化 Web 界面**：使用 Gradio 构建直观易用的 Web UI，支持跨平台访问
2. **快速文件生成**：高效的块写入算法，快速生成任意大小的文件（KB/MB/GB/TB）
3. **实时磁盘监控**：实时显示磁盘使用情况，支持多种单位切换
4. **智能错误处理**：完善的输入验证和错误提示，包括磁盘空间检查
5. **跨平台支持**：支持 Windows、macOS、Linux 系统
6. **完善的测试覆盖**：使用 pytest 进行单元测试，确保代码质量
7. **日志记录**：完整的日志系统，便于问题排查

## 🚀 快速开始

### 环境要求

- Python >= 3.11
- 依赖包：`psutil`, `gradio`

### 安装

使用 `uv` 包管理器（推荐）：

```bash
# 安装依赖
uv sync

# 运行应用
uv run python main.py
```

或使用传统方式：

```bash
# 安装依赖（从 pyproject.toml）
pip install -e .

# 或直接安装依赖包
pip install psutil>=7.1.3 gradio>=4.0.0

# 运行应用
python main.py
```

详细安装说明请查看 [安装指南](docs/installation.md)。

### 使用说明

1. 启动应用后，浏览器会自动打开（默认地址：`http://localhost:7860`）
2. 在"文件生成设置"区域：
   - 输入保存路径（例如：`/Users/username/Downloads`）
   - 输入文件名称（例如：`test_file.bin`）
   - 输入文件大小并选择单位（KB/MB/GB/TB）
3. 点击"开始生成文件"按钮
4. 在"磁盘空间监控"区域实时查看磁盘使用情况

详细使用说明请查看 [使用指南](docs/usage.md)。

## 📁 项目结构

```
FileTools/
├── main.py                 # 主入口文件
├── pyproject.toml          # 项目配置和依赖管理
├── LICENSE                 # MIT 许可证
├── docs/                   # 文档目录
│   ├── CHANGELOG.md        # 版本变更记录
│   ├── English_README.md   # 英文 README
│   ├── contributing.md     # 贡献指南
│   ├── development.md      # 开发指南
│   ├── installation.md     # 安装指南
│   ├── usage.md            # 使用指南
│   ├── testing.md          # 测试文档
│   ├── logging.md          # 日志文档
│   └── faq.md              # 常见问题
├── src/                    # 源代码目录
│   └── filetools/          # 主包
│       ├── __init__.py
│       ├── config/         # 配置模块
│       │   ├── __init__.py
│       │   ├── constants.py # 常量定义
│       │   └── logger.py   # 日志配置
│       ├── models/          # 业务逻辑模块
│       │   ├── __init__.py
│       │   ├── file_generator.py  # 文件生成逻辑
│       │   ├── disk_monitor.py    # 磁盘监控逻辑
│       │   └── disk_usage.py      # 磁盘使用情况数据模型
│       └── ui/              # UI 模块
│           ├── __init__.py
│           └── interface.py # Gradio 界面组件
├── tests/                  # 测试模块
│   ├── __init__.py
│   ├── test_constants.py
│   ├── test_disk_monitor.py
│   ├── test_file_generator.py
│   ├── test_file_generator_core.py
│   ├── test_ui_functions.py
│   └── test_ui_validation.py
├── docs/                   # 文档目录
│   ├── installation.md    # 安装指南
│   ├── usage.md           # 使用指南
│   ├── development.md     # 开发指南
│   ├── testing.md         # 测试文档
│   ├── logging.md         # 日志文档
│   ├── faq.md             # 常见问题
│   └── contributing.md    # 贡献指南
├── assets/                 # 资源文件目录
│   └── 扫码_搜索联合传播样式-白色版.png
└── .github/                # GitHub 配置
    └── workflows/
        └── ci.yml          # CI 工作流
```

完整项目结构说明请查看 [开发指南](docs/development.md)。

## 🔧 技术架构

- **前端框架**：Gradio（Python Web UI 框架）
- **系统监控**：psutil（跨平台系统监控库）
- **文件操作**：Python 标准库 `pathlib`, `io`
- **测试框架**：pytest
- **架构模式**：模块化设计，清晰的职责分离

## 💡 核心特性

### 文件生成

- 支持 KB、MB、GB、TB 四种单位
- 使用块写入算法（100MB 块），提高生成速度
- 自动验证文件大小和磁盘空间
- 完善的错误处理和提示
- 支持进度回调，实时显示生成进度

### 磁盘监控

- 实时显示所有磁盘分区的使用情况
- 智能过滤系统分区（macOS/Windows）
- 支持多种显示单位切换（KB/MB/GB/TB）
- 显示使用率、已用空间、可用空间、总空间
- 自动刷新和手动刷新两种模式

## 📚 文档

- [安装指南](docs/installation.md) - 详细的安装说明和环境配置
- [使用指南](docs/usage.md) - 功能使用说明和示例
- [开发指南](docs/development.md) - 开发环境设置和代码规范
- [测试文档](docs/testing.md) - 测试运行和编写指南
- [日志文档](docs/logging.md) - 日志配置和查看方法
- [常见问题](docs/faq.md) - FAQ 和故障排除
- [贡献指南](docs/contributing.md) - 如何为项目做贡献

## 🧪 测试

项目使用 `pytest` 进行单元测试。运行测试：

```bash
# 使用 uv 运行测试（推荐）
uv run pytest

# 运行测试并显示覆盖率
uv run pytest --cov=models --cov=ui --cov=config
```

详细测试说明请查看 [测试文档](docs/testing.md)。

## ❓ 常见问题

遇到问题？请先查看 [常见问题文档](docs/faq.md)。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！详细说明请查看 [贡献指南](docs/contributing.md)。

- 📝 [提交 Issue](https://github.com/fishzjp/FileTools/issues)
- 🔀 [提交 Pull Request](https://github.com/fishzjp/FileTools/pulls)
- 📦 [项目仓库](https://github.com/fishzjp/FileTools)

## 📄 许可证

本项目采用 MIT 许可证。

## 📱 公众号

![扫码_搜索联合传播样式-白色版](assets/扫码_搜索联合传播样式-白色版.png)

---

希望这个工具对你有帮助！如有任何问题或建议，欢迎反馈。
