"""磁盘使用情况数据模型"""
from dataclasses import dataclass


@dataclass
class DiskUsage:
    """
    磁盘使用情况数据模型
    
    :param device: 设备名称
    :param total: 总空间（字节）
    :param used: 已用空间（字节）
    :param percent: 使用百分比
    """
    device: str
    total: int
    used: int
    percent: float

