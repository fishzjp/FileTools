"""Gradio界面组件"""
import gradio as gr
from pathlib import Path
from typing import List, Tuple
from filetools.config.constants import DEFAULT_UNIT, UNIT_MAPPING
from filetools.config.logger import logger
from filetools.models.file_generator import generate_file_with_progress
from filetools.models.disk_monitor import get_disk_usage_info
from filetools.models.disk_usage import DiskUsage


def format_disk_size(size: float, unit: str) -> str:
    """格式化磁盘大小"""
    return f"{size:.2f} {unit}"


def format_disk_info(disk_usages: List[DiskUsage], unit: str) -> str:
    """
    格式化磁盘信息为Markdown
    
    :param disk_usages: 磁盘使用情况列表
    :param unit: 显示单位
    :return: Markdown格式的磁盘信息
    """
    if not disk_usages:
        return "暂无磁盘信息"
    
    divider = UNIT_MAPPING[unit]
    markdown_parts = []
    
    for disk_usage in disk_usages:
        current_space = disk_usage.used / divider
        available_space = (disk_usage.total - disk_usage.used) / divider
        total_space = disk_usage.total / divider
        
        markdown = f"""
### 💿 {disk_usage.device}
**使用率**: {disk_usage.percent:.1f}%
- **已用**: {format_disk_size(current_space, unit)}
- **可用**: {format_disk_size(available_space, unit)}
- **总计**: {format_disk_size(total_space, unit)}

---
"""
        markdown_parts.append(markdown)
    
    return "\n".join(markdown_parts)


def update_disk_display(unit: str) -> str:
    """
    更新磁盘显示
    
    :param unit: 显示单位
    :return: Markdown格式的磁盘信息
    """
    logger.info(f"更新磁盘显示，单位: {unit}")
    disk_usages = get_disk_usage_info()
    return format_disk_info(disk_usages, unit)


def _validate_inputs(dir_path: str, file_name: str, file_size_str: str) -> Tuple[bool, str]:
    """
    验证输入参数
    
    :param dir_path: 保存目录路径
    :param file_name: 文件名
    :param file_size_str: 文件大小字符串
    :return: (是否有效, 错误消息)
    """
    if not dir_path or not file_name or not file_size_str:
        return False, "❌ 错误：所有输入框都必须填写！"
    return True, ""


def _validate_directory(dir_path: str) -> Tuple[bool, str, Path]:
    """
    验证目录路径
    
    :param dir_path: 目录路径
    :return: (是否有效, 错误消息, Path对象)
    """
    try:
        dir_path_obj = Path(dir_path)
        if not dir_path_obj.exists() or not dir_path_obj.is_dir():
            return False, f"❌ 错误：目录不存在：{dir_path}", dir_path_obj
        return True, "", dir_path_obj
    except Exception as e:
        return False, f"❌ 错误：无效的目录路径：{str(e)}", Path(dir_path)


def _validate_file_size(file_size_str: str) -> Tuple[bool, str, int]:
    """
    验证文件大小
    
    :param file_size_str: 文件大小字符串
    :return: (是否有效, 错误消息, 文件大小)
    """
    try:
        file_size = int(file_size_str)
        if file_size <= 0:
            return False, "❌ 错误：文件大小必须大于0！", 0
        return True, "", file_size
    except ValueError:
        return False, "❌ 错误：文件大小必须是一个整数！", 0


def generate_file_handler(
    dir_path: str,
    file_name: str,
    file_size_str: str,
    file_size_unit: str,
    disk_unit: str,
) -> Tuple[str, str]:
    """
    文件生成处理函数
    
    :param dir_path: 保存目录路径
    :param file_name: 文件名
    :param file_size_str: 文件大小字符串
    :param file_size_unit: 文件大小单位
    :param disk_unit: 磁盘显示单位
    :return: (结果消息, 磁盘信息Markdown)
    """
    logger.info(f"收到文件生成请求: 目录={dir_path}, 文件名={file_name}, 大小={file_size_str} {file_size_unit}")
    
    # 验证输入
    is_valid, error_msg = _validate_inputs(dir_path, file_name, file_size_str)
    if not is_valid:
        logger.warning(f"输入验证失败: {error_msg}")
        return error_msg, update_disk_display(disk_unit)
    
    # 验证目录
    is_valid, error_msg, dir_path_obj = _validate_directory(dir_path)
    if not is_valid:
        logger.warning(f"目录验证失败: {error_msg}")
        return error_msg, update_disk_display(disk_unit)
    
    # 验证文件大小
    is_valid, error_msg, file_size = _validate_file_size(file_size_str)
    if not is_valid:
        logger.warning(f"文件大小验证失败: {error_msg}")
        return error_msg, update_disk_display(disk_unit)
    
    # 构建完整文件路径
    file_path = dir_path_obj / file_name
    
    # 检查文件是否已存在
    if file_path.exists():
        error_msg = f"❌ 错误：文件已存在：{file_path}"
        logger.warning(error_msg)
        return error_msg, update_disk_display(disk_unit)
    
    # 生成文件
    result = generate_file_with_progress(str(file_path), file_size, file_size_unit, None)
    
    # 更新磁盘信息
    disk_info = update_disk_display(disk_unit)
    
    if "成功" in result:
        success_msg = f"✅ {result}\n文件路径: {file_path}"
        logger.info(success_msg)
        return success_msg, disk_info
    else:
        logger.error(f"文件生成失败: {result}")
        return f"❌ {result}", disk_info


def create_interface():
    """创建Gradio界面"""
    with gr.Blocks(title="文件大小生成工具") as app:
        gr.Markdown(
            """
            # 📁 文件大小生成工具
            
            用于生成指定大小的文件，并实时监控磁盘空间使用情况。
            """
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                # 文件生成设置区域
                with gr.Group():
                    gr.Markdown("### 📁 文件生成设置")
                    
                    dir_path_input = gr.Textbox(
                        label="保存路径",
                        placeholder="例如: /Users/username/Downloads 或 C:\\Users\\username\\Downloads",
                        value="",
                    )
                    
                    file_name_input = gr.Textbox(
                        label="文件名称",
                        placeholder="例如: test_file",
                        value="",
                    )
                    
                    with gr.Row():
                        file_size_input = gr.Textbox(
                            label="文件大小",
                            placeholder="输入大小",
                            scale=3,
                            value="",
                        )
                        file_size_unit = gr.Dropdown(
                            choices=["KB", "MB", "GB", "TB"],
                            value=DEFAULT_UNIT,
                            scale=1,
                            label="单位",
                        )
                    
                    generate_btn = gr.Button("开始生成文件", variant="primary", size="lg")
                
                # 生成进度和结果
                with gr.Group():
                    gr.Markdown("### ⚙️ 文件生成进度")
                    
                    result_output = gr.Textbox(
                        label="生成结果",
                        value="",
                        interactive=False,
                        lines=3,
                    )
            
            with gr.Column(scale=1):
                # 磁盘监控区域
                with gr.Group():
                    gr.Markdown("### 💾 磁盘空间监控")
                    
                    disk_unit = gr.Dropdown(
                        choices=["KB", "MB", "GB", "TB"],
                        value=DEFAULT_UNIT,
                        label="显示单位",
                    )
                    
                    disk_info_md = gr.Markdown(
                        value=update_disk_display(DEFAULT_UNIT),
                        label="",
                    )
                    
                    refresh_btn = gr.Button("刷新", variant="secondary")
        
        # 事件绑定
        generate_btn.click(
            fn=generate_file_handler,
            inputs=[dir_path_input, file_name_input, file_size_input, file_size_unit, disk_unit],
            outputs=[result_output, disk_info_md],
        )
        
        disk_unit_state = gr.State(value=DEFAULT_UNIT)
        
        def update_disk_with_unit(unit: str) -> str:
            """更新磁盘显示并保存单位状态"""
            disk_unit_state.value = unit
            return update_disk_display(unit)
        
        def auto_refresh() -> str:
            """自动刷新磁盘信息"""
            return update_disk_display(disk_unit_state.value)
        
        disk_unit.change(
            fn=update_disk_with_unit,
            inputs=[disk_unit],
            outputs=[disk_info_md],
        )
        
        refresh_btn.click(
            fn=update_disk_with_unit,
            inputs=[disk_unit],
            outputs=[disk_info_md],
        )
        
        # 自动刷新磁盘信息（页面加载时）
        app.load(
            fn=auto_refresh,
            outputs=[disk_info_md],
        )
    
    return app
