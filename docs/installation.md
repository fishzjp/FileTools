# 📦 安装指南

## 环境要求

- Python >= 3.11
- 依赖包：`psutil`, `gradio`

## 安装方式

### 方式一：使用 uv 包管理器（推荐）

```bash
# 安装依赖
uv sync

# 运行应用
uv run python main.py
```

### 方式二：使用传统方式

```bash
# 安装依赖（从 pyproject.toml）
pip install -e .

# 或直接安装依赖包
pip install psutil>=7.1.3 gradio>=4.0.0

# 运行应用
python main.py
```

## 开发环境设置

如果需要参与开发，需要安装开发依赖：

```bash
# 使用 uv 安装开发依赖（包括 pytest）
uv sync --extra dev

# 或使用传统方式
pip install -e ".[dev]"
```

## 验证安装

安装完成后，可以通过以下方式验证：

```bash
# 检查 Python 版本
python --version

# 检查依赖是否安装
python -c "import psutil, gradio; print('Dependencies installed successfully')"
```

## 常见安装问题

### 问题：uv 命令未找到

**解决方案：**
- macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

### 问题：pip 安装失败

**解决方案：**
1. 确保 Python 版本 >= 3.11
2. 升级 pip: `python -m pip install --upgrade pip`
3. 使用虚拟环境隔离依赖

### 问题：权限错误

**解决方案：**
- 使用虚拟环境避免权限问题
- macOS/Linux: 不要使用 `sudo` 安装 Python 包

