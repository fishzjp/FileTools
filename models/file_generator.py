"""文件生成业务逻辑"""
from pathlib import Path
from typing import Callable, Optional
from config.constants import CHUNK_SIZE, UNIT_MAPPING


def generate_file(file_path: str, file_size_bytes: int, progress_callback: Optional[Callable[[int], int]] = None) -> None:
    """
    生成指定大小的文件
    
    使用单线程顺序写入，因为文件I/O通常是磁盘带宽限制的，多线程并不会提升性能。
    
    :param file_path: 文件路径
    :param file_size_bytes: 文件大小（字节）
    :param progress_callback: 进度回调函数，参数为当前进度(0-100)，返回更新后的进度
    """
    path = Path(file_path)
    
    # 确保父目录存在
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # 计算块数
    total_chunks = file_size_bytes // CHUNK_SIZE
    last_chunk_size = file_size_bytes % CHUNK_SIZE
    total_size = file_size_bytes
    
    written = 0
    
    # 使用二进制追加模式创建文件
    with open(path, 'wb') as file:
        # 写入完整块
        for i in range(total_chunks):
            file.write(b'\0' * CHUNK_SIZE)
            written += CHUNK_SIZE
            
            # 更新进度
            if progress_callback:
                progress = int((written / total_size) * 100)
                progress_callback(progress)
        
        # 写入最后一个不完整的块
        if last_chunk_size > 0:
            file.write(b'\0' * last_chunk_size)
            written += last_chunk_size
    
    # 确保最终进度为100%
    if progress_callback:
        progress_callback(100)


def generate_file_with_progress(
    file_path: str, 
    file_size: int, 
    unit: str, 
    progress_callback: Optional[Callable[[int], int]] = None
) -> str:
    """
    执行文件生成，包含单位转换和错误处理
    
    :param file_path: 文件路径
    :param file_size: 文件大小数值
    :param unit: 单位（KB, MB, GB, TB）
    :param progress_callback: 进度回调函数，参数为当前进度(0-100)
    :return: 结果消息
    """
    try:
        # 验证单位
        if unit not in UNIT_MAPPING:
            raise ValueError(f"不支持的单位: {unit}。支持的单位: {', '.join(UNIT_MAPPING.keys())}")
        
        # 验证文件大小
        if file_size <= 0:
            raise ValueError("文件大小必须大于0")
        
        # 根据单位转换文件大小为字节
        unit_multiplier = UNIT_MAPPING[unit]
        file_size_bytes = file_size * unit_multiplier
        
        # 检查磁盘空间（粗略检查，避免创建超大文件导致系统问题）
        try:
            from utils.disk import get_disk_usages
            disk_usages = get_disk_usages()
            if disk_usages:
                # 检查第一个磁盘的可用空间
                _, total, used, _ = disk_usages[0]
                available = total - used
                if file_size_bytes > available:
                    return f"文件生成失败：磁盘空间不足。需要 {file_size_bytes / (1024**3):.2f} GB，可用 {available / (1024**3):.2f} GB"
        except Exception:
            # 如果无法检查磁盘空间，继续执行（可能是权限问题）
            pass
        
        # 执行文件生成
        generate_file(file_path, file_size_bytes, progress_callback)
        
        # 验证文件是否成功创建
        path = Path(file_path)
        if not path.exists():
            return "文件生成失败：文件创建后未找到"
        
        actual_size = path.stat().st_size
        if actual_size != file_size_bytes:
            return f"文件生成失败：文件大小不匹配。期望 {file_size_bytes} 字节，实际 {actual_size} 字节"
        
        return "文件生成成功！"
    except ValueError as e:
        return f"文件生成失败：{str(e)}"
    except PermissionError:
        return f"文件生成失败：没有权限写入文件或目录"
    except OSError as e:
        return f"文件生成失败：系统错误 - {str(e)}"
    except Exception as e:
        return f"文件生成失败：未知错误 - {str(e)}"

