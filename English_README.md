# Background

In the process of software development and system testing, it is often necessary to test the performance and handling capabilities of a system when the disk space is full. Such testing scenarios help developers and testers evaluate the robustness and performance of the system in resource-constrained environments. However, manually creating large files and filling up the disk is a tedious and time-consuming task. To simplify this process and improve efficiency, I have developed a file generation tool that can create files of arbitrary sizes according to requirements, simulating a scenario where the disk space is full.

# Project Features

1. User-friendly interface: This tool utilizes the PyQt5 library to create a graphical interface, allowing users to operate intuitively and conveniently. The interface provides input fields for folder path, file name, file size, as well as browse and generate buttons, enabling users to easily choose paths and set file parameters.
2. Fast file writing speed: Instantaneous writing of files of any size.

# Program Packaging

### The program is packaged using pyinstaller, with the option of using upx compression. The packaging commands are as follows:
```
# Packaging command with upx compression - Note: Replace --upx-dir= with the installation path of upx on your local machine
pyinstaller --onefile --add-data "icon.png;." --add-data "SmileySans-Oblique.ttf;." --add-data "style.qss;." --noconsole --upx-dir=D:\code\file_tools\tools\upx-4.0.2-win64\upx-4.0.2-win64 file_tools.py

# Packaging command without upx compression
pyinstaller --onefile --add-data "icon.png;." --add-data "SmileySans-Oblique.ttf;." --add-data "style.qss;." --noconsole file_tools.py
```

# Tool Interface

![image](https://github.com/fishzjp/FileTools/assets/105406371/5cb835f9-def3-4a29-bcb4-b5db637a9146)

# Tool Download ![](https://img.shields.io/github/v/release/fishzjp/FileTools?style=flat-square) 
https://github.com/fishzjp/FileTools/releases

# Tool Font
The font used is Smiley Sans, available at https://github.com/atelier-anchor/smiley-sans

# WeChat Public Account
![QR Code](https://github.com/fishzjp/FileTools/assets/105406371/49abfbc1-d46e-410c-98f1-959f2dbfe87a)

<br> I hope this optimization is helpful for you. If there are any other areas that need improvement, please feel free to let me know.
