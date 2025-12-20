"""UI 验证函数测试"""
import pytest
import tempfile
import os
import time
import sys
from pathlib import Path
from filetools.ui.interface import _validate_inputs, _validate_directory, _validate_file_size


class TestUIValidation:
    """UI 验证函数测试类"""
    
    def test_validate_inputs_all_valid(self):
        """测试所有输入有效"""
        is_valid, error_msg = _validate_inputs("/tmp", "test.bin", "100")
        assert is_valid is True
        assert error_msg == ""
    
    def test_validate_inputs_empty_dir_path(self):
        """测试空目录路径"""
        is_valid, error_msg = _validate_inputs("", "test.bin", "100")
        assert is_valid is False
        assert "必须填写" in error_msg
    
    def test_validate_inputs_empty_file_name(self):
        """测试空文件名"""
        is_valid, error_msg = _validate_inputs("/tmp", "", "100")
        assert is_valid is False
        assert "必须填写" in error_msg
    
    def test_validate_inputs_empty_file_size(self):
        """测试空文件大小"""
        is_valid, error_msg = _validate_inputs("/tmp", "test.bin", "")
        assert is_valid is False
        assert "必须填写" in error_msg
    
    def test_validate_directory_exists(self):
        """测试存在的目录"""
        with tempfile.TemporaryDirectory() as tmpdir:
            is_valid, error_msg, path_obj = _validate_directory(tmpdir)
            assert is_valid is True
            assert error_msg == ""
            assert isinstance(path_obj, Path)
    
    def test_validate_directory_not_exists(self):
        """测试不存在的目录"""
        fake_dir = "/nonexistent/directory/path"
        is_valid, error_msg, path_obj = _validate_directory(fake_dir)
        assert is_valid is False
        assert "不存在" in error_msg
    
    def test_validate_directory_file_not_dir(self):
        """测试路径是文件而不是目录"""
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile_path = tmpfile.name
            try:
                is_valid, error_msg, path_obj = _validate_directory(tmpfile_path)
                assert is_valid is False
                assert "不存在" in error_msg or "目录" in error_msg
            finally:
                # Windows 上文件可能被锁定，需要重试删除
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        Path(tmpfile_path).unlink()
                        break
                    except (PermissionError, OSError) as e:
                        if attempt < max_retries - 1:
                            time.sleep(0.1)  # 等待文件句柄释放
                        else:
                            # Windows 上如果文件仍被锁定，忽略错误
                            if sys.platform == "win32":
                                pass  # Windows 上允许删除失败
                            else:
                                raise  # 其他平台抛出异常
    
    def test_validate_file_size_valid(self):
        """测试有效的文件大小"""
        is_valid, error_msg, size = _validate_file_size("100")
        assert is_valid is True
        assert error_msg == ""
        assert size == 100
    
    def test_validate_file_size_zero(self):
        """测试文件大小为0"""
        is_valid, error_msg, size = _validate_file_size("0")
        assert is_valid is False
        assert "必须大于0" in error_msg
    
    def test_validate_file_size_negative(self):
        """测试文件大小为负数"""
        is_valid, error_msg, size = _validate_file_size("-1")
        assert is_valid is False
        assert "必须大于0" in error_msg
    
    def test_validate_file_size_not_integer(self):
        """测试文件大小不是整数"""
        is_valid, error_msg, size = _validate_file_size("abc")
        assert is_valid is False
        assert "整数" in error_msg
    
    def test_validate_file_size_float_string(self):
        """测试文件大小为浮点数字符串"""
        is_valid, error_msg, size = _validate_file_size("100.5")
        assert is_valid is False
        assert "整数" in error_msg
    
    def test_validate_file_size_large_number(self):
        """测试大数字"""
        is_valid, error_msg, size = _validate_file_size("999999999")
        assert is_valid is True
        assert size == 999999999

