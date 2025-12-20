"""磁盘监控功能测试"""
import pytest
from filetools.models.disk_monitor import get_disk_usage_info
from filetools.models.disk_usage import DiskUsage


class TestDiskMonitor:
    """磁盘监控测试类"""
    
    def test_get_disk_usage_info_returns_list(self):
        """测试返回列表类型"""
        result = get_disk_usage_info()
        assert isinstance(result, list)
    
    def test_get_disk_usage_info_contains_disk_usage(self):
        """测试返回 DiskUsage 对象"""
        result = get_disk_usage_info()
        if result:  # 如果有磁盘信息
            assert isinstance(result[0], DiskUsage)
    
    def test_disk_usage_has_required_fields(self):
        """测试 DiskUsage 对象包含必需字段"""
        result = get_disk_usage_info()
        if result:
            disk = result[0]
            assert hasattr(disk, 'device')
            assert hasattr(disk, 'total')
            assert hasattr(disk, 'used')
            assert hasattr(disk, 'percent')
            assert isinstance(disk.device, str)
            assert isinstance(disk.total, int)
            assert isinstance(disk.used, int)
            assert isinstance(disk.percent, float)
    
    def test_disk_usage_percent_range(self):
        """测试使用百分比在合理范围内"""
        result = get_disk_usage_info()
        if result:
            for disk in result:
                assert 0 <= disk.percent <= 100
    
    def test_disk_usage_total_positive(self):
        """测试总空间为正数"""
        result = get_disk_usage_info()
        if result:
            for disk in result:
                assert disk.total > 0
    
    def test_disk_usage_used_positive(self):
        """测试已用空间为正数或0"""
        result = get_disk_usage_info()
        if result:
            for disk in result:
                assert disk.used >= 0
    
    def test_disk_usage_used_not_exceed_total(self):
        """测试已用空间不超过总空间"""
        result = get_disk_usage_info()
        if result:
            for disk in result:
                assert disk.used <= disk.total
    
    def test_get_disk_usage_info_multiple_calls(self):
        """测试多次调用返回一致结果"""
        result1 = get_disk_usage_info()
        result2 = get_disk_usage_info()
        assert len(result1) == len(result2)
    
    def test_disk_usage_device_not_empty(self):
        """测试设备名称不为空"""
        result = get_disk_usage_info()
        if result:
            for disk in result:
                assert disk.device and len(disk.device) > 0

