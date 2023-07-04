import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QLineEdit, QPushButton, QMessageBox, QFileDialog
)
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtCore import Qt


def generate_file(file_path, file_size):
    file_size_bytes = file_size * 1024 * 1024
    path = Path(file_path)
    path.touch()
    path.write_bytes(b'\0' * file_size_bytes)
    return f"文件已生成：{file_path}，大小：{file_size}MB"


def resource_path(relative_path):
    """获取资源的绝对路径"""
    if hasattr(sys, '_MEIPASS'):
        # 如果是打包后的可执行文件
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class FileGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('任意大小文件生成器')
        self.setWindowIcon(QIcon(resource_path('icon.png')))  # 设置图标
        self.setFixedSize(320, 380)  # 设置固定大小
        self.setup_ui()

    def setup_ui(self):
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

        generate_button = QPushButton('生成文件')
        generate_button.clicked.connect(self.generate_button_clicked)

        layout.addWidget(path_label)
        layout.addWidget(self.path_input)
        layout.addWidget(browse_button)
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(size_label)
        layout.addWidget(self.size_input)
        layout.addWidget(generate_button)

        # 添加版权信息标签
        copyright_label = QLabel(
            "© 2023 zjp. All rights reserved. Unauthorized copying, modification, distribution, or any form of use of this work is strictly prohibited. Violators will be held liable under the law. version 1.0.0.1."
        )
        copyright_label.setStyleSheet("font-size: 12px; color: #888888;")
        copyright_label.setWordWrap(True)  # 设置自动换行
        layout.addWidget(copyright_label)

        self.setLayout(layout)

        # 加载并注册字体
        font_id = QFontDatabase.addApplicationFont(resource_path('SmileySans-Oblique.ttf'))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        # 设置全局字体
        app_font = QFont(font_family)
        app_font.setPointSize(16)
        QApplication.instance().setFont(app_font)

        # 设置窗口样式
        self.setStyleSheet(
            """
            QWidget {
                background-color: #FFF;
            }

            QLabel {
                font-family: '%s';
                font-size: 16px;
            }

            QLineEdit {
                border: 1px solid #DADADA;
                border-radius: 5px;
                padding: 5px;
                font-family: '%s';
                font-size: 14px;
            }

            QPushButton {
                border: none;
                padding: 5px 10px;
                color: #FFFFFF;
                background-color: #007BFF;
                border-radius: 5px;
                font-family: '%s';
                font-size: 16px;
            }

            QPushButton:hover {
                background-color: #0056b3;
            }

            QPushButton:pressed {
                background-color: #004080;
            }
        """
            % (font_family, font_family, font_family)
        )

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
            result = generate_file(file_path, file_size)
            QMessageBox.information(self, '生成成功', result, QMessageBox.Ok)
        except ValueError:
            QMessageBox.warning(self, '警告', '文件大小必须是一个整数！', QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, '生成失败', str(e), QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileGeneratorApp()
    window.show()
    sys.exit(app.exec_())
