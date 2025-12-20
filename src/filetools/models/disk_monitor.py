"""磁盘监控业务逻辑"""
import os
import psutil
import platform
from typing import List

from filetools.config.constants import MIN_DISK_SIZE
from filetools.config.logger import logger
from filetools.models.disk_usage import DiskUsage


def _should_skip_partition_macos(mountpoint: str, partition_opts: str) -> bool:
    """
    判断 macOS 分区是否应该跳过
    
    :param mountpoint: 挂载点路径
    :param partition_opts: 分区选项
    :return: 是否跳过
    """
    # 跳过特定的系统卷（但保留Data卷，它是主数据卷）
    skip_volumes = [
        '/System/Volumes/Preboot',
        '/System/Volumes/Update',
        '/System/Volumes/VM',
        '/System/Volumes/xarts',
        '/System/Volumes/iSCPreboot',
        '/System/Volumes/Hardware',
        '/private/var/vm',  # 虚拟内存
    ]
    # 使用精确匹配而不是包含匹配，避免误过滤子路径
    if mountpoint in skip_volumes or any(mountpoint.startswith(skip + '/') for skip in skip_volumes):
        return True
    
    # 对于根分区 `/`，如果是只读的，跳过它（数据在 /System/Volumes/Data）
    if mountpoint == '/' and 'ro' in partition_opts:
        return True
    
    # 跳过其他只读分区（但保留 /System/Volumes/Data 和 /Volumes 下的外部卷）
    if 'ro' in partition_opts:
        # 保留数据卷和外部卷
        if mountpoint == '/System/Volumes/Data' or mountpoint.startswith('/Volumes/'):
            return False  # 不跳过
        else:
            return True  # 跳过
    
    return False


def _get_device_name_macos(mountpoint: str) -> str:
    """
    获取 macOS 设备友好名称
    
    :param mountpoint: 挂载点路径
    :return: 设备名称
    """
    if mountpoint.startswith('/Volumes/'):
        # 外部卷，从路径提取卷名，例如: /Volumes/Macintosh HD -> "Macintosh HD"
        return os.path.basename(mountpoint.rstrip('/'))
    elif mountpoint == '/System/Volumes/Data':
        # 主系统数据卷，使用友好名称
        return 'Macintosh HD'
    elif mountpoint == '/':
        # 根分区（如果还没被过滤）
        return 'Macintosh HD'
    else:
        # 其他挂载点，使用挂载点路径的最后一部分
        return os.path.basename(mountpoint.rstrip('/')) or '系统盘'


def _get_device_name(partition: psutil._common.sdiskpart, is_macos: bool) -> str:
    """
    获取设备友好名称
    
    :param partition: 分区对象
    :param is_macos: 是否为 macOS 系统
    :return: 设备名称
    """
    if is_macos:
        return _get_device_name_macos(partition.mountpoint)
    else:
        # Windows/Linux: 使用设备名
        return partition.device if partition.device else partition.mountpoint


def get_disk_usage_info() -> List[DiskUsage]:
    """
    获取磁盘使用情况
    
    :return: 磁盘使用情况列表
    """
    logger.info("开始获取磁盘使用情况")
    disk_usages = []
    partitions = psutil.disk_partitions(all=False)  # 只获取已挂载的分区
    
    # macOS特定处理
    is_macos = platform.system() == 'Darwin'
    seen_mountpoints = set()
    
    for partition in partitions:
        try:
            # Windows: 跳过CD-ROM
            if os.name == 'nt' and 'cdrom' in partition.opts:
                continue
            
            mountpoint = partition.mountpoint
            
            # 避免重复挂载点
            if mountpoint in seen_mountpoints:
                continue
            
            # macOS: 过滤系统分区
            if is_macos and _should_skip_partition_macos(mountpoint, partition.opts):
                continue
            
            usage = psutil.disk_usage(mountpoint)
            
            # 跳过总空间为0或很小的分区（可能是伪设备）
            if usage.total < MIN_DISK_SIZE:
                logger.debug(f"跳过小分区: {mountpoint} (总空间: {usage.total} 字节)")
                continue
            
            # 获取设备友好名称
            device_name = _get_device_name(partition, is_macos)
            
            disk_usage = DiskUsage(
                device=device_name,
                total=usage.total,
                used=usage.used,
                percent=usage.percent
            )
            disk_usages.append(disk_usage)
            seen_mountpoints.add(mountpoint)
            
        except (PermissionError, OSError) as e:
            # 跳过没有权限访问的分区
            logger.warning(f"无法访问分区 {partition.mountpoint}: {e}")
            continue
        except Exception as e:
            logger.error(f"获取分区信息时发生未知错误 {partition.mountpoint}: {e}")
            continue
    
    logger.info(f"成功获取 {len(disk_usages)} 个磁盘的使用情况")
    return disk_usages
