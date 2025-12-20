# 🧪 测试文档

## 概述

项目使用 `pytest` 进行单元测试，确保代码质量和功能正确性。

## 运行测试

### 基本命令

```bash
# 使用 uv 运行测试（推荐）
uv run pytest

# 或使用传统方式
pytest
```

### 详细输出

```bash
# 运行测试并显示详细输出
uv run pytest -v

# 显示更详细的信息
uv run pytest -vv
```

### 运行特定测试

```bash
# 运行特定测试文件
uv run pytest tests/test_file_generator.py

# 运行特定测试类
uv run pytest tests/test_file_generator.py::TestFileGenerator

# 运行特定测试方法
uv run pytest tests/test_file_generator.py::TestFileGenerator::test_generate_file_success_kb
```

### 测试覆盖率

```bash
# 运行测试并显示覆盖率
uv run pytest --cov=models --cov=ui --cov=config

# 生成覆盖率报告
uv run pytest --cov=models --cov=ui --cov=config --cov-report=html
```

覆盖率报告会生成在 `htmlcov/` 目录下。

## 测试覆盖

### 已覆盖的模块

- ✅ 常量定义测试 (`test_constants.py`)
- ✅ 文件生成功能测试 (`test_file_generator.py`, `test_file_generator_core.py`)
- ✅ 磁盘监控功能测试 (`test_disk_monitor.py`)
- ✅ UI 验证函数测试 (`test_ui_validation.py`)
- ✅ UI 功能函数测试 (`test_ui_functions.py`)
- ✅ 错误处理测试

### 测试文件说明

#### test_constants.py
测试常量定义的正确性，包括单位映射、块大小等。

#### test_file_generator.py
测试文件生成功能，包括：
- 不同单位的文件生成（KB/MB/GB/TB）
- 错误处理（无效单位、零大小等）

#### test_file_generator_core.py
测试文件生成核心功能，包括进度回调等。

#### test_disk_monitor.py
测试磁盘监控功能，包括：
- 磁盘信息获取
- 单位转换
- 系统分区过滤

#### test_ui_validation.py
测试 UI 输入验证功能。

#### test_ui_functions.py
测试 UI 功能函数。

## 编写测试

### 测试文件结构

```python
"""模块功能测试"""
import pytest
from module import function


class TestModule:
    """模块测试类"""
    
    def test_function_success(self):
        """测试功能成功场景"""
        result = function(param1, param2)
        assert result == expected_value
    
    def test_function_failure(self):
        """测试功能失败场景"""
        with pytest.raises(ValueError):
            function(invalid_param)
```

### 测试命名规范

- 测试文件：`test_*.py`
- 测试类：`Test*`
- 测试方法：`test_*`

### 使用 pytest fixtures

```python
import pytest
import tempfile

@pytest.fixture
def temp_dir():
    """临时目录 fixture"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir
```

### 参数化测试

```python
@pytest.mark.parametrize("size,unit,expected", [
    (1, "KB", 1024),
    (1, "MB", 1024 * 1024),
    (1, "GB", 1024 * 1024 * 1024),
])
def test_size_conversion(size, unit, expected):
    """测试大小转换"""
    result = convert_size(size, unit)
    assert result == expected
```

## 测试最佳实践

1. **独立性**：每个测试应该独立运行，不依赖其他测试
2. **可重复性**：测试结果应该可重复
3. **快速执行**：测试应该快速执行
4. **清晰命名**：测试名称应该清晰描述测试内容
5. **完整覆盖**：尽可能覆盖所有代码路径

## 持续集成

建议在 CI/CD 流程中运行测试：

```yaml
# .github/workflows/test.yml 示例
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: uv sync
      - run: uv run pytest
```

