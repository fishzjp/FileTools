"""磁盘使用情况工具"""
import os
import psutil
import platform
from typing import List, Tuple


def get_disk_usages() -> List[Tuple[str, int, int, float]]:
    """
    获取磁盘使用情况
    
    :return: 磁盘使用情况列表，每个元素为(设备名, 总空间, 已用空间, 使用百分比)
    """
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
            if is_macos:
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
                    continue
                
                # 对于根分区 `/`，如果是只读的，跳过它（数据在 /System/Volumes/Data）
                # 这样可以避免显示重复的磁盘信息
                if mountpoint == '/' and 'ro' in partition.opts:
                    continue
                
                # 跳过其他只读分区（但保留 /System/Volumes/Data 和 /Volumes 下的外部卷）
                if 'ro' in partition.opts:
                    # 保留数据卷和外部卷
                    if mountpoint == '/System/Volumes/Data' or mountpoint.startswith('/Volumes/'):
                        pass  # 不跳过
                    else:
                        continue
            
            usage = psutil.disk_usage(mountpoint)
            
            # 跳过总空间为0或很小的分区（可能是伪设备）
            if usage.total < 1024 * 1024:  # 小于1MB
                continue
            
            # macOS: 使用更友好的显示名称
            if is_macos:
                if mountpoint.startswith('/Volumes/'):
                    # 外部卷，从路径提取卷名，例如: /Volumes/Macintosh HD -> "Macintosh HD"
                    device_name = os.path.basename(mountpoint.rstrip('/'))
                elif mountpoint == '/System/Volumes/Data':
                    # 主系统数据卷，使用友好名称
                    device_name = 'Macintosh HD'
                elif mountpoint == '/':
                    # 根分区（如果还没被过滤）
                    device_name = 'Macintosh HD'
                else:
                    # 其他挂载点，使用挂载点路径的最后一部分
                    device_name = os.path.basename(mountpoint.rstrip('/')) or '系统盘'
            else:
                # Windows/Linux: 使用设备名
                device_name = partition.device if partition.device else mountpoint
            
            disk_usages.append((device_name, usage.total, usage.used, usage.percent))
            seen_mountpoints.add(mountpoint)
            
        except (PermissionError, OSError):
            # 跳过没有权限访问的分区
            continue
    
    return disk_usages

