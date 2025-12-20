"""文件生成核心功能测试（测试 generate_file 函数）"""
import pytest
import tempfile
import os
from filetools.models.file_generator import generate_file
from filetools.config.constants import CHUNK_SIZE


class TestFileGeneratorCore:
    """文件生成核心函数测试类"""
    
    def test_generate_file_basic(self):
        """测试基本文件生成"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test.bin")
            generate_file(file_path, 1024, None)
            assert os.path.exists(file_path)
            assert os.path.getsize(file_path) == 1024
    
    def test_generate_file_exact_chunk_size(self):
        """测试生成恰好一个块大小的文件"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test_chunk.bin")
            generate_file(file_path, CHUNK_SIZE, None)
            assert os.path.exists(file_path)
            assert os.path.getsize(file_path) == CHUNK_SIZE
    
    def test_generate_file_multiple_chunks(self):
        """测试生成多个块的文件"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test_multi.bin")
            size = CHUNK_SIZE * 2
            generate_file(file_path, size, None)
            assert os.path.exists(file_path)
            assert os.path.getsize(file_path) == size
    
    def test_generate_file_partial_chunk(self):
        """测试生成小于一个块的文件"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test_partial.bin")
            size = CHUNK_SIZE // 2
            generate_file(file_path, size, None)
            assert os.path.exists(file_path)
            assert os.path.getsize(file_path) == size
    
    def test_generate_file_with_remainder(self):
        """测试生成带余数的文件（不是块的整数倍）"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test_remainder.bin")
            size = CHUNK_SIZE * 2 + 1000
            generate_file(file_path, size, None)
            assert os.path.exists(file_path)
            assert os.path.getsize(file_path) == size
    
    def test_generate_file_progress_callback(self):
        """测试进度回调函数"""
        progress_values = []
        
        def progress_callback(progress: int) -> int:
            progress_values.append(progress)
            return progress
        
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test_progress.bin")
            size = CHUNK_SIZE * 2
            generate_file(file_path, size, progress_callback)
            assert os.path.exists(file_path)
            assert len(progress_values) > 0
            assert progress_values[-1] == 100  # 最终进度应该是100%
            # 进度应该是递增的
            for i in range(1, len(progress_values)):
                assert progress_values[i] >= progress_values[i-1]
    
    def test_generate_file_creates_nested_dirs(self):
        """测试自动创建嵌套目录"""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = os.path.join(tmpdir, "level1", "level2", "level3")
            file_path = os.path.join(nested_path, "test.bin")
            generate_file(file_path, 1024, None)
            assert os.path.exists(file_path)
            assert os.path.isdir(nested_path)
    
    def test_generate_file_zero_size(self):
        """测试生成0字节文件"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test_zero.bin")
            generate_file(file_path, 0, None)
            assert os.path.exists(file_path)
            assert os.path.getsize(file_path) == 0

