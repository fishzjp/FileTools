import sys
import os
import psutil
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QMessageBox, QFileDialog, QProgressBar
)
from PyQt5.QtGui import QIcon, QFont, QFontDatabase, QPainter, QColor, QPalette
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QThreadPool, QRunnable

# Rest of the code remains unchanged..

def resource_path(relative_path):
    """获取资源的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        # 如果是打包后的可执行文件
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

class CustomApplication(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_custom_font()

    def load_custom_font(self):
        # Load the custom font file
        font_path = resource_path('SmileySans-Oblique.ttf')
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family)
            self.setFont(font)

class DiskUsageProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_style()  # 使用主界面的样式
        self.setTextVisible(False)

    def load_style(self):
        style_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'style.qss')
        with open(style_file, 'r', encoding='utf-8') as f:  # 指定编码为 UTF-8
            style = f.read()
            self.setStyleSheet(style)

    def paintEvent(self, event):
        progress = 100 * self.value() / self.maximum()
        text = f'{progress:.1f}%'
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 计算进度条的高度和宽度
        height = self.height() - 6  # 将高度减小
        width = self.width() * (progress / 100)

        # 绘制带圆角的矩形作为进度条的背景
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.lightGray)
        painter.drawRoundedRect(2, 2, self.width() - 4, height, 8, 8)

        # 绘制带圆角的矩形表示进度
        if width > 0:
            painter.setBrush(Qt.blue)
            painter.drawRoundedRect(2, 2, width, height, 8, 8)

        # 绘制文本
        font = QFont()
        font.setPointSize(13)
        painter.setFont(font)
        painter.setPen(Qt.white)
        painter.drawText(self.rect(), Qt.AlignCenter, text)

    def setValue(self, progress):
        super().setValue(progress)

class DiskUsageWidget(QWidget):
    def __init__(self, device, total, used, percent):
        super().__init__()
        self.device = device
        self.total = total
        self.used = used
        self.percent = percent

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title_label = QLabel(f"{self.device} 盘空间使用情况")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        self.disk_bar = DiskUsageProgressBar()
        self.disk_bar.setValue(self.percent)
        layout.addWidget(self.disk_bar)

        self.current_space_label = QLabel()
        self.current_space_label.setAlignment(Qt.AlignCenter)  # Align text to center
        self.update_current_space()
        layout.addWidget(self.current_space_label)

        self.setLayout(layout)

    def update_current_space(self):
        current_space = self.used / (1024 * 1024 * 1024)
        available_space = (self.total - self.used) / (1024 * 1024 * 1024)
        total_space = self.total / (1024 * 1024 * 1024)
        text = f" Used {current_space:.2f} GB / Free {available_space:.2f} GB / Total {total_space:.2f} GB"

        self.current_space_label.setStyleSheet("font-size: 14px; color: #999999;")  # Set font size to 8pt and color to gray
        self.current_space_label.setAlignment(Qt.AlignCenter)  # Align text to center
        self.current_space_label.setText(text)

    def update_usage(self, used, percent):
        self.used = used
        self.percent = percent
        self.disk_bar.setValue(self.percent)
        self.update_current_space()

def get_disk_usages():
    disk_usages = []
    partitions = psutil.disk_partitions(all=True)
    for partition in partitions:
        if os.name == 'nt' and 'cdrom' in partition.opts:
            # 跳过 Windows 上的光驱
            continue
        usage = psutil.disk_usage(partition.mountpoint)
        disk_usages.append((partition.device, usage.total, usage.used, usage.percent))
    return disk_usages

class DiskUsageThread(QThread):
    disk_usages_signal = pyqtSignal(list)

    def run(self):
        while True:
            disk_usages = get_disk_usages()
            self.disk_usages_signal.emit(disk_usages)
            # 每次更新后延迟一秒
            self.msleep(1000)

def generate_chunk(file_path, chunk_size):
    with open(file_path, 'wb') as file:
        file.write(b'\0' * chunk_size)

def generate_file(file_path, file_size, progress_callback):
    file_size_bytes = file_size * 1024 * 1024
    chunk_size = 100 * 1024 * 1024  # 100 MB 为一块 (可根据需要调整)
    total_chunks = file_size_bytes // chunk_size

    # 预分配文件空间
    Path(file_path).touch()

    for i in range(total_chunks):
        generate_chunk(file_path, chunk_size)
        progress = (i + 1) / total_chunks * 100
        progress_callback.emit(progress)

    progress_callback.emit(100)

class FileGeneratorThread(QThread):
    generation_completed = pyqtSignal(str)
    progress_callback = pyqtSignal(int)

    def __init__(self, file_path, file_size):
        super().__init__()
        self.file_path = file_path
        self.file_size = file_size

    def run(self):
        try:
            file_size_bytes = self.file_size * 1024 * 1024
            chunk_size = 100 * 1024 * 1024  # 100 MB 为一块 (可根据需要调整)
            total_chunks = file_size_bytes // chunk_size

            # 预分配文件空间
            Path(self.file_path).touch()

            for i in range(total_chunks):
                self.generate_chunk(self.file_path, chunk_size)
                progress = (i + 1) / total_chunks * 100
                self.progress_callback.emit(progress)

            self.progress_callback.emit(100)
            self.generation_completed.emit("文件生成成功！")
        except Exception as e:
            self.generation_completed.emit(f"文件生成失败：{str(e)}")

    def generate_chunk(self, file_path, chunk_size):
        with open(file_path, 'ab') as file:
            file.write(b'\0' * chunk_size)



class FileGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('任意大小文件生成器')
        self.setWindowIcon(QIcon(resource_path('icon.png')))
        self.setMinimumSize(390, 0)  # 设置最小宽度，高度自动调整
        self.setMaximumSize(390, 0)

        self.disk_usage_widgets = []  # 存储磁盘部件的列表

        # 创建 DiskUsageThread 的实例，并将其信号连接到 update_disk_usages 槽
        self.disk_usage_thread = DiskUsageThread(self)
        self.disk_usage_thread.disk_usages_signal.connect(self.update_disk_usages)
        self.disk_usage_thread.start()

        # 初始化 QThreadPool
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(1)  # 限制同时只能运行一个生成文件任务

        self.progress_bar = QProgressBar()  # 添加 progress_bar 属性
        self.init_ui()

        # 加载样式表
        self.load_style()

        # 设置应用程序的自定义字体
        font_path = resource_path('SmileySans-Oblique.ttf')
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family)
            QApplication.setFont(font)

        # 设置主窗口的自定义字体
        self.setFont(QFont(font_family))

    def load_style(self):
        style_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'style.qss')
        with open(style_file, 'r', encoding='utf-8') as f:  # 指定编码为 UTF-8
            style = f.read()

        # Load the custom font file
        font_path = resource_path('SmileySans-Oblique.ttf')
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            style += f"\n* {{ font-family: '{font_family}'; }}"

        # Apply the custom style sheet to the main application and all widgets
        self.setStyleSheet(style)
        for widget in QApplication.allWidgets():
            widget.setStyleSheet(style)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        path_label = QLabel('文件夹路径:')
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText('选择文件夹路径')

        browse_button = QPushButton('浏览')
        browse_button.clicked.connect(self.browse_button_clicked)

        name_label = QLabel('文件名称:')
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('输入文件名称')

        size_label = QLabel('文件大小(MB):')
        self.size_input = QLineEdit()
        self.size_input.setPlaceholderText('输入文件大小')

        self.disk_dashboard_label = QLabel('磁盘空间使用情况：')

        # 使用一个独立的布局来容纳磁盘空间使用情况的部件
        disk_usage_layout = QVBoxLayout()

        disk_usages = get_disk_usages()
        for disk_usage in disk_usages:
            device, total, used, percent = disk_usage
            disk_widget = DiskUsageWidget(device, total, used, percent)
            self.disk_usage_widgets.append(disk_widget)
            disk_usage_layout.addWidget(disk_widget)

        layout.addWidget(path_label)
        layout.addWidget(self.path_input)
        layout.addWidget(browse_button)
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(size_label)
        layout.addWidget(self.size_input)

        # 将磁盘空间使用情况的标签和部件添加到主布局中，这样它们会显示在文件大小输入框下方
        layout.addWidget(self.disk_dashboard_label)
        layout.addLayout(disk_usage_layout)  # 将包含磁盘部件的布局添加到主布局中

        # 添加生成文件进度标题和进度条
        generate_layout = QVBoxLayout()
        self.progress_label = QLabel('文件生成进度：')
        generate_layout.addWidget(self.progress_label)
        generate_layout.addWidget(self.progress_bar)

        # 添加生成文件按钮
        generate_button = QPushButton('生成文件')
        generate_button.clicked.connect(self.generate_button_clicked)
        generate_layout.addWidget(generate_button)  # 将生成文件按钮添加到布局中

        layout.addLayout(generate_layout)  # Add the layout containing progress and button to the main layout

        # 添加主布局到窗口
        self.setLayout(layout)

    def browse_button_clicked(self):
        dir_path = QFileDialog.getExistingDirectory(self, '选择文件夹路径')
        self.path_input.setText(dir_path)

    def generate_button_clicked(self):
        dir_path = self.path_input.text()
        file_name = self.name_input.text()
        file_size = self.size_input.text()

        if not dir_path or not file_name or not file_size:
            QMessageBox.warning(self, '警告', '所有输入框都必须填写！', QMessageBox.Ok)
            return

        try:
            file_size = int(file_size)
            file_path = f"{dir_path}/{file_name}"

            self.file_generator_thread = FileGeneratorThread(file_path, file_size)
            self.file_generator_thread.generation_completed.connect(self.file_generation_completed)
            self.file_generator_thread.progress_callback.connect(self.update_progress_bar)

            # 使用 QThread 启动文件生成线程
            self.file_generator_thread.start()
        except ValueError:
            QMessageBox.warning(self, '警告', '文件大小必须是一个整数！', QMessageBox.Ok)


    def file_generation_completed(self, message):
        QMessageBox.information(self, '生成结果', message, QMessageBox.Ok)

    def update_progress_bar(self, progress):
        self.progress_bar.setValue(progress)

    def update_disk_usages(self, disk_usages):
        # 删除原有的磁盘空间使用情况部件
        for widget in self.disk_usage_widgets:
            widget.setParent(None)

        # 清空存储的部件列表
        self.disk_usage_widgets = []

        # 使用一个独立的布局来容纳磁盘空间使用情况的部件
        disk_usage_layout = QVBoxLayout()

        for disk_usage in disk_usages:
            device, total, used, percent = disk_usage
            disk_widget = DiskUsageWidget(device, total, used, percent)
            self.disk_usage_widgets.append(disk_widget)
            disk_usage_layout.addWidget(disk_widget)

        # 将磁盘空间使用情况的标签和部件添加到主布局中，这样它们会显示在文件大小输入框下方
        layout = self.layout()
        layout.insertWidget(layout.count() - 2, self.disk_dashboard_label)
        layout.insertLayout(layout.count() - 1, disk_usage_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 设置样式为 Fusion 风格
    custom_app = CustomApplication(sys.argv)  # 使用自定义字体的应用程序实例
    window = FileGeneratorApp()
    window.show()
    sys.exit(app.exec_())
