"""UI 函数测试"""
import pytest
from filetools.ui.interface import format_disk_size, format_disk_info, update_disk_display
from filetools.models.disk_usage import DiskUsage


class TestUIFunctions:
    """UI 函数测试类"""
    
    def test_format_disk_size(self):
        """测试格式化磁盘大小"""
        result = format_disk_size(1.5, "GB")
        assert result == "1.50 GB"
        
        result = format_disk_size(0.123, "MB")
        assert result == "0.12 MB"
        
        result = format_disk_size(100.0, "KB")
        assert result == "100.00 KB"
    
    def test_format_disk_info_empty_list(self):
        """测试空列表格式化"""
        result = format_disk_info([], "GB")
        assert result == "暂无磁盘信息"
    
    def test_format_disk_info_single_disk(self):
        """测试单个磁盘格式化"""
        disk = DiskUsage(
            device="Test Disk",
            total=1024 * 1024 * 1024,  # 1GB
            used=512 * 1024 * 1024,     # 512MB
            percent=50.0
        )
        result = format_disk_info([disk], "GB")
        assert "Test Disk" in result
        assert "50.0%" in result
        assert "0.50 GB" in result  # 已用
        assert "0.50 GB" in result  # 可用
        assert "1.00 GB" in result  # 总计
    
    def test_format_disk_info_multiple_disks(self):
        """测试多个磁盘格式化"""
        disks = [
            DiskUsage(device="Disk1", total=1024**3, used=512*1024**2, percent=50.0),
            DiskUsage(device="Disk2", total=2*1024**3, used=1024**3, percent=50.0),
        ]
        result = format_disk_info(disks, "GB")
        assert "Disk1" in result
        assert "Disk2" in result
        assert result.count("###") == 2  # 两个磁盘标题
    
    def test_format_disk_info_different_units(self):
        """测试不同单位的格式化"""
        disk = DiskUsage(
            device="Test Disk",
            total=1024 * 1024 * 1024,  # 1GB
            used=512 * 1024 * 1024,     # 512MB
            percent=50.0
        )
        
        result_mb = format_disk_info([disk], "MB")
        assert "512.00 MB" in result_mb  # 已用
        
        result_kb = format_disk_info([disk], "KB")
        assert "KB" in result_kb
    
    def test_update_disk_display(self):
        """测试更新磁盘显示"""
        result = update_disk_display("GB")
        assert isinstance(result, str)
        # 结果应该包含磁盘信息或"暂无磁盘信息"
        assert len(result) > 0
    
    def test_update_disk_display_different_units(self):
        """测试不同单位的磁盘显示"""
        units = ["KB", "MB", "GB", "TB"]
        for unit in units:
            result = update_disk_display(unit)
            assert isinstance(result, str)
            assert len(result) > 0

