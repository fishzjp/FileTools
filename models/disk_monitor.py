"""磁盘监控业务逻辑"""
from typing import List, Tuple
from utils.disk import get_disk_usages


def get_disk_usage_info() -> List[Tuple[str, int, int, float]]:
    """
    获取磁盘使用情况
    
    :return: 磁盘使用情况列表，每个元素为(设备名, 总空间, 已用空间, 使用百分比)
    """
    return get_disk_usages()
