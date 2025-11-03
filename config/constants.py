"""常量配置"""
from typing import Dict

# 单位映射（字节数）
UNIT_MAPPING: Dict[str, int] = {
    "KB": 1024,
    "MB": 1024 * 1024,
    "GB": 1024 * 1024 * 1024,
    "TB": 1024 * 1024 * 1024 * 1024
}

# 文件生成块大小（100MB）
CHUNK_SIZE: int = 100 * 1024 * 1024

# 默认单位
DEFAULT_UNIT: str = "GB"

