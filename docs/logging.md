# 📝 日志文档

## 概述

项目使用 Python 标准库 `logging` 进行日志记录，日志同时输出到控制台和文件。

## 日志配置

### 配置位置

日志配置在 `config/logger.py` 文件中。

### 配置参数

- **日志文件位置**：`logs/filetools.log`
- **日志级别**：INFO（可在 `config/logger.py` 中修改）
- **日志格式**：`时间 - 名称 - 级别 - 消息`
- **编码**：UTF-8

### 日志级别

- **DEBUG**：详细的调试信息
- **INFO**：一般信息（默认级别）
- **WARNING**：警告信息
- **ERROR**：错误信息
- **CRITICAL**：严重错误

### 修改日志级别

编辑 `config/logger.py`：

```python
# 修改为 DEBUG 级别
logger = setup_logger(level=logging.DEBUG)

# 修改为 WARNING 级别
logger = setup_logger(level=logging.WARNING)
```

## 查看日志

### 命令行查看

```bash
# 查看实时日志
tail -f logs/filetools.log

# 查看最近 100 行日志
tail -n 100 logs/filetools.log

# 查看所有日志
cat logs/filetools.log

# 在 Windows 上查看日志
type logs\filetools.log

# 在 Windows 上查看最近 100 行
powershell "Get-Content logs\filetools.log -Tail 100"
```

### 搜索日志

```bash
# 搜索错误日志
grep ERROR logs/filetools.log

# 搜索特定关键词
grep "文件生成" logs/filetools.log

# 在 Windows 上搜索
findstr "ERROR" logs\filetools.log
```

## 日志内容

### 记录的信息

日志记录包括：
- 应用启动和关闭
- 文件生成开始和完成
- 磁盘监控操作
- 错误和异常信息
- 用户操作记录

### 日志格式示例

```
2025-12-20 12:00:00 - filetools - INFO - 启动文件大小生成工具
2025-12-20 12:00:01 - filetools - INFO - Gradio 界面已创建，正在启动服务器...
2025-12-20 12:00:05 - filetools - INFO - 开始生成文件: /path/to/file.bin, 大小: 1073741824 字节
2025-12-20 12:00:10 - filetools - INFO - 文件生成成功: /path/to/file.bin
2025-12-20 12:00:15 - filetools - ERROR - 文件生成失败: 磁盘空间不足
```

## 日志管理

### 日志轮转

当前版本未实现自动日志轮转。如果日志文件过大，可以：

1. **手动清理**：定期删除或归档旧日志文件
2. **配置日志轮转**：修改 `config/logger.py` 使用 `RotatingFileHandler`

### 配置日志轮转示例

```python
from logging.handlers import RotatingFileHandler

# 创建轮转文件处理器（最大 10MB，保留 5 个备份）
file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=5,
    encoding="utf-8"
)
```

### 日志文件位置

日志文件默认保存在项目根目录的 `logs/` 目录下。如果目录不存在，会自动创建。

### 禁用日志

如果需要禁用文件日志（仅保留控制台输出），可以修改 `config/logger.py`：

```python
# 注释掉文件处理器
# logger.addHandler(file_handler)
```

## 最佳实践

1. **合理使用日志级别**：根据信息重要性选择合适的级别
2. **记录关键操作**：记录用户操作和系统状态变化
3. **记录错误详情**：错误日志应包含足够的上下文信息
4. **避免敏感信息**：不要在日志中记录密码、密钥等敏感信息
5. **定期清理**：定期清理或归档旧日志文件

## 调试技巧

### 启用调试模式

```python
# 在代码中临时启用 DEBUG 级别
import logging
logger.setLevel(logging.DEBUG)
```

### 添加自定义日志

```python
from config.logger import logger

# 记录信息
logger.info("操作完成")

# 记录警告
logger.warning("磁盘空间不足")

# 记录错误
logger.error("文件生成失败", exc_info=True)

# 记录调试信息
logger.debug("变量值: %s", variable)
```

