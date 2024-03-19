import sys
import os
import psutil
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QFileDialog, QProgressBar, QRadioButton, QGroupBox
from PyQt5.QtGui import QIcon, QFont, QFontDatabase, QPainter, QColor, QPalette
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QToolTip
import concurrent.futures

def resource_path(relative_path):
    """
    获取资源路径，用于处理打包后的资源路径
    :param relative_path: 相对路径
    :return: 完整的资源路径
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

class CustomApplication(QApplication):
    """
    自定义应用程序类，用于加载自定义字体
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_custom_font()

    def load_custom_font(self):
        """
        加载自定义字体
        """
        font_path = resource_path('SmileySans-Oblique.ttf')
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family)
            self.setFont(font)

class DiskUsageProgressBar(QProgressBar):
    """
    自定义磁盘使用进度条类
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_style()
        self.setTextVisible(False)

    def load_style(self):
        """
        加载样式表
        """
        style_file = resource_path('style.qss')
        with open(style_file, 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def paintEvent(self, event):
        """
        重写绘制事件，自定义绘制进度条
        """
        progress = 100 * self.value() / self.maximum()
        text = f'{progress:.1f}%'
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        height = int(self.height() - 3)
        width = int(self.width() * (progress / 100))
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.lightGray)
        painter.drawRoundedRect(2, 2, self.width() - 4, height, 8, 8)
        if width > 0:
            painter.setBrush(Qt.blue)
            painter.drawRoundedRect(2, 2, width, height, 8, 8)

        painter.setPen(Qt.white)
        painter.drawText(self.rect(), Qt.AlignCenter, text)

    def setValue(self, progress):
        """
        设置进度值
        """
        super().setValue(int(progress))

class DiskUsageWidget(QWidget):
    """
    磁盘使用情况小部件类
    """
    def __init__(self, device, total, used, percent, unit):
        super().__init__()
        self.device = device
        self.total = total
        self.used = used
        self.percent = percent
        self.current_unit = unit
        self.init_ui()

    def init_ui(self):
        """
        初始化用户界面
        """
        layout = QVBoxLayout()
        title_label = QLabel(f"{self.device} 盘空间使用情况")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        self.disk_bar = DiskUsageProgressBar()
        self.disk_bar.setValue(self.percent)
        layout.addWidget(self.disk_bar)

        self.current_space_label = QLabel()
        self.current_space_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.current_space_label)

        self.setLayout(layout)

    def set_unit(self, unit):
        """
        设置单位
        """
        self.current_unit = unit

    def update_current_space(self):
        """
        更新当前空间信息
        """
        unit_mapping = {"KB": 1024, "MB": 1024 * 1024, "GB": 1024 * 1024 * 1024, "TB": 1024 * 1024 * 1024 * 1024}
        selected_unit = self.current_unit

        current_space = self.used / unit_mapping[selected_unit]
        available_space = (self.total - self.used) / unit_mapping[selected_unit]
        total_space = self.total / unit_mapping[selected_unit]

        text = f"{current_space:.2f} {selected_unit[0]}B / {available_space:.2f} {selected_unit[0]}B / {total_space:.2f} {selected_unit[0]}B"
        self.current_space_label.setStyleSheet("font-size: 12px; color: #999999;")
        self.current_space_label.setAlignment(Qt.AlignCenter)
        self.current_space_label.setText(text)
        self.current_space_label.setToolTip(f"已用空间：{current_space:.2f} {selected_unit}\n"
                                             f"剩余空间：{available_space:.2f} {selected_unit}\n"
                                             f"总空间：{total_space:.2f} {selected_unit}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_current_space()

    def enterEvent(self, event):
        # Override the enterEvent to force showing the tooltip when the mouse enters
        QToolTip.showText(event.globalPos(), self.current_space_label.toolTip(), self.current_space_label)

    def leaveEvent(self, event):
        # Override the leaveEvent to reset the tooltip when the mouse leaves
        QToolTip.hideText()

def get_disk_usages():
    """
    获取磁盘使用情况
    """
    disk_usages = []
    partitions = psutil.disk_partitions(all=True)
    for partition in partitions:
        if os.name == 'nt' and 'cdrom' in partition.opts:
            continue
        usage = psutil.disk_usage(partition.mountpoint)
        disk_usages.append((partition.device, usage.total, usage.used, usage.percent))
    return disk_usages

class DiskUsageThread(QThread):
    """
    磁盘使用情况线程类
    """
    disk_usages_signal = pyqtSignal(list)

    def run(self):
        while True:
            disk_usages = get_disk_usages()
            self.disk_usages_signal.emit(disk_usages)
            self.msleep(1000)

def generate_chunk(file_path, chunk_size):
    """
    生成文件块
    """
    with open(file_path, 'wb') as file:
        file.write(b'\0' * chunk_size)

def generate_file(file_path, file_size, progress_callback):
    """
    生成文件
    """
    file_size_bytes = file_size * 1024 * 1024
    chunk_size = 100 * 1024 * 1024
    total_chunks = file_size_bytes // chunk_size
    Path(file_path).touch()

    for i in range(total_chunks):
        generate_chunk(file_path, chunk_size)
        progress = (i + 1) / total_chunks * 100
        progress_callback.emit(progress)

    progress_callback.emit(100)

class FileGeneratorThread(QThread):
    """
    文件生成线程类
    """
    generation_completed = pyqtSignal(str)
    progress_callback = pyqtSignal(int)

    def __init__(self, file_path, file_size, unit):
        super().__init__()
        self.file_path = file_path
        self.file_size = file_size
        self.unit = unit

    def generate_chunk(self, file_path, chunk_size):
        with open(file_path, 'ab') as file:
            file.write(b'\0' * chunk_size)

    def generate_file(self, total_chunks, chunk_size):
        max_workers = max(os.cpu_count() - 1, 1)  # 根据系统CPU核数动态设置max_workers
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.generate_chunk, self.file_path, chunk_size) for _ in range(total_chunks)]

            for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
                progress = (i / total_chunks) * 100
                self.progress_callback.emit(progress)
                future.result()

    def run(self):
        try:
            file_size_bytes = self.file_size * 1024 * 1024
            chunk_size = 100 * 1024 * 1024
            total_chunks = file_size_bytes // chunk_size
            last_chunk_size = file_size_bytes % chunk_size

            Path(self.file_path).touch()

            self.generate_file(total_chunks, chunk_size)

            if last_chunk_size > 0:
                self.generate_chunk(self.file_path, last_chunk_size)
                self.progress_callback.emit(100)

            self.generation_completed.emit("文件生成成功！")
        except Exception as e:
            self.generation_completed.emit(f"文件生成失败：{str(e)}")

class FileGeneratorApp(QWidget):
    """
    文件生成应用程序主窗口类
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('任意大小文件生成器')
        self.setWindowIcon(QIcon(resource_path('icon.png')))
        self.setMinimumSize(390, 800)
        self.setMaximumSize(390, 800)

        self.disk_usage_widgets = []
        self.disk_usage_thread = DiskUsageThread(self)
        self.disk_usage_thread.disk_usages_signal.connect(self.update_disk_usages)
        self.disk_usage_thread.start()

        self.progress_bar = QProgressBar()
        self.unit_group = QGroupBox('磁盘空间单位')
        self.unit_radio_buttons = []
        self.current_unit = "GB"  # 初始化默认单位为GB
        self.init_ui()

        self.load_style()

        font_path = resource_path('SmileySans-Oblique.ttf')
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.setFont(QFont(font_family))
            QApplication.setFont(QFont(font_family))  # 这里也要设置应用程序的字体

    def load_style(self):
        """
        加载样式表
        """
        style_file = resource_path('style.qss')
        with open(style_file, 'r', encoding='utf-8') as f:
            style = f.read()

        font_path = resource_path('SmileySans-Oblique.ttf')
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            style += f"\n* {{ font-family: '{font_family}'; }}"

        self.setStyleSheet(style)

        font = QFont(font_family)
        for widget in QApplication.allWidgets():
            widget.setFont(font)
            widget.setStyleSheet(style)

    def init_ui(self):
        """
        初始化用户界面
        """
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

        size_label = QLabel('文件大小:')
        self.size_input = QLineEdit()
        self.size_input.setPlaceholderText('输入文件大小')

        self.disk_dashboard_label = QLabel('磁盘空间使用情况：')
        disk_usage_layout = QVBoxLayout()

        disk_usages = get_disk_usages()
        for disk_usage in disk_usages:
            device, total, used, percent = disk_usage
            disk_widget = DiskUsageWidget(device, total, used, percent, self.current_unit)
            self.disk_usage_widgets.append(disk_widget)
            disk_usage_layout.addWidget(disk_widget)

        layout.addWidget(path_label)
        layout.addWidget(self.path_input)
        layout.addWidget(browse_button)
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(size_label)
        layout.addWidget(self.size_input)
        layout.addWidget(self.disk_dashboard_label)
        layout.addLayout(disk_usage_layout)

        unit_layout = QHBoxLayout()
        self.unit_group = QGroupBox('磁盘空间单位')
        self.unit_radio_buttons.append(self.create_radio_button("KB"))
        self.unit_radio_buttons.append(self.create_radio_button("MB"))
        self.unit_radio_buttons.append(self.create_radio_button("GB"))
        self.unit_radio_buttons.append(self.create_radio_button("TB"))
        unit_layout.addWidget(self.unit_radio_buttons[0])
        unit_layout.addWidget(self.unit_radio_buttons[1])
        unit_layout.addWidget(self.unit_radio_buttons[2])
        unit_layout.addWidget(self.unit_radio_buttons[3])
        self.unit_group.setLayout(unit_layout)
        layout.addWidget(self.unit_group)

        for radio_button in self.unit_radio_buttons:
            radio_button.toggled.connect(self.on_unit_changed)

        generate_layout = QVBoxLayout()
        self.progress_label = QLabel('文件生成进度：')
        generate_layout.addWidget(self.progress_label)
        generate_layout.addWidget(self.progress_bar)

        generate_button = QPushButton('生成文件')
        generate_button.clicked.connect(self.generate_button_clicked)
        generate_layout.addWidget(generate_button)

        layout.addLayout(generate_layout)
        self.setLayout(layout)

    def create_radio_button(self, text):
        """
        创建单选按钮
        """
        radio_button = QRadioButton(text)
        radio_button.setChecked(text == "GB")
        return radio_button

    def on_unit_changed(self):
        """
        单位改变事件处理函数
        """
        selected_unit = ""
        for radio_button in self.unit_radio_buttons:
            if radio_button.isChecked():
                selected_unit = radio_button.text()
                break

        self.current_unit = selected_unit

        for widget in self.disk_usage_widgets:
            widget.set_unit(selected_unit)
            widget.update_current_space()

    def browse_button_clicked(self):
        """
        浏览按钮点击事件处理函数
        """
        dir_path = QFileDialog.getExistingDirectory(self, '选择文件夹路径')
        self.path_input.setText(dir_path)

    def generate_button_clicked(self):
        """
        生成文件按钮点击事件处理函数
        """
        dir_path = self.path_input.text()
        file_name = self.name_input.text()
        file_size = self.size_input.text()

        if not dir_path or not file_name or not file_size:
            QMessageBox.warning(self, '警告', '所有输入框都必须填写！', QMessageBox.Ok)
            return

        try:
            file_size = int(file_size)
            selected_unit = ""
            for radio_button in self.unit_radio_buttons:
                if radio_button.isChecked():
                    selected_unit = radio_button.text()
                    break

            file_path = f"{dir_path}/{file_name}"

            self.file_generator_thread = FileGeneratorThread(file_path, file_size, selected_unit)
            self.file_generator_thread.generation_completed.connect(self.file_generation_completed)
            self.file_generator_thread.progress_callback.connect(self.update_progress_bar)

            self.file_generator_thread.start()
        except ValueError:
            QMessageBox.warning(self, '警告', '文件大小必须是一个整数！', QMessageBox.Ok)

    def file_generation_completed(self, message):
        """
        文件生成完成处理函数
        """
        QMessageBox.information(self, '生成结果', message, QMessageBox.Ok)

    def update_progress_bar(self, progress):
        """
        更新进度条
        """
        self.progress_bar.setValue(progress)

    def update_disk_usages(self, disk_usages):
        """
        更新磁盘使用情况
        """
        for widget in self.disk_usage_widgets:
            widget.setParent(None)
        self.disk_usage_widgets = []
        disk_usage_layout = QVBoxLayout()
        for disk_usage in disk_usages:
            device, total, used, percent = disk_usage
            disk_widget = DiskUsageWidget(device, total, used, percent, self.current_unit)
            self.disk_usage_widgets.append(disk_widget)
            disk_usage_layout.addWidget(disk_widget)
        layout = self.layout()
        layout.insertWidget(layout.count() - 2, self.disk_dashboard_label)
        layout.insertLayout(layout.count() - 1, disk_usage_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    custom_app = CustomApplication(sys.argv)
    window = FileGeneratorApp()
    window.show()
    sys.exit(app.exec_())
