"""常量配置测试"""
import pytest
from filetools.config.constants import (
    UNIT_MAPPING,
    CHUNK_SIZE,
    DEFAULT_UNIT,
    MIN_DISK_SIZE,
)


class TestConstants:
    """常量配置测试类"""
    
    def test_unit_mapping_keys(self):
        """测试单位映射的键"""
        assert "KB" in UNIT_MAPPING
        assert "MB" in UNIT_MAPPING
        assert "GB" in UNIT_MAPPING
        assert "TB" in UNIT_MAPPING
    
    def test_unit_mapping_values(self):
        """测试单位映射的值"""
        assert UNIT_MAPPING["KB"] == 1024
        assert UNIT_MAPPING["MB"] == 1024 * 1024
        assert UNIT_MAPPING["GB"] == 1024 * 1024 * 1024
        assert UNIT_MAPPING["TB"] == 1024 * 1024 * 1024 * 1024
    
    def test_unit_mapping_relationships(self):
        """测试单位之间的换算关系"""
        assert UNIT_MAPPING["MB"] == UNIT_MAPPING["KB"] * 1024
        assert UNIT_MAPPING["GB"] == UNIT_MAPPING["MB"] * 1024
        assert UNIT_MAPPING["TB"] == UNIT_MAPPING["GB"] * 1024
    
    def test_chunk_size(self):
        """测试块大小"""
        assert CHUNK_SIZE == 100 * 1024 * 1024  # 100MB
        assert CHUNK_SIZE > 0
    
    def test_default_unit(self):
        """测试默认单位"""
        assert DEFAULT_UNIT in UNIT_MAPPING
        assert DEFAULT_UNIT == "GB"
    
    def test_min_disk_size(self):
        """测试最小磁盘大小"""
        assert MIN_DISK_SIZE == 1024 * 1024  # 1MB
        assert MIN_DISK_SIZE > 0

