# 背景

在软件开发和系统测试的过程中，经常需要测试在磁盘空间满的情况下系统的表现和处理能力。这样的测试场景可以帮助开发人员和测试人员评估系统在资源紧张的环境下的鲁棒性和性能。
然而，手动创建大文件并将磁盘填满是一项繁琐且耗时的任务。为了简化这个过程并提高效率，我开发了一个文件生成工具，该工具可以根据需求创建任意大小的文件，以模拟磁盘空间满的场景。

# 项目特点

1. 用户友好的界面：该工具使用了PyQt5库来创建一个图形化界面，使用户能够直观、方便地操作。界面提供了文件夹路径、文件名称和文件大小等输入框，以及浏览和生成按钮，用户可以轻松选择路径和设置文件参数。
2. 文件写入速度快：任意大小文件秒写入

# 程序打包

### 程序使用pyinstaller打包，打包时有使用upx压缩，打包命令如下
```
# 使用upx压缩打包命令  注意：--upx-dir= 需要替换为你本地upx的安装路径
pyinstaller --onefile --add-data "icon.png;." --add-data "SmileySans-Oblique.ttf;." --add-data "style.qss;." --noconsole --upx-dir=D:\code\file_tools\tools\upx-4.0.2-win64\upx-4.0.2-win64 file_tools.py

# 不使用upx压缩打包命令
pyinstaller --onefile --add-data "icon.png;." --add-data "SmileySans-Oblique.ttf;." --add-data "style.qss;." --noconsole file_tools.py
```

# 工具界面

v 1.1.0.2<br>
![image](https://github.com/fishzjp/FileTools/assets/105406371/5cb835f9-def3-4a29-bcb4-b5db637a9146)

<br>
v 1.1.0.1<br>

![image](https://github.com/fishzjp/FileTools/assets/105406371/6c740942-dbde-4d2f-ac06-39b527de94d4)

<br>
v 1.0.0.1<br>

![image](https://github.com/fishzjp/FileTools/assets/105406371/f8c8b563-ba67-46f5-8083-b7e876c405c4)


# 工具字体
字体采用得意黑 https://github.com/atelier-anchor/smiley-sans

# Relese
  ### v1.1.0.3
    1. 优化文件写入速度 写入速度提升40%
    2. 优化部分已知问题
  ### v1.1.0.2
    1. 增加磁盘剩余空间单位的选择
    2. 优化部分已知问题
  ### v1.1.0.1 
    1. 增加动态磁盘剩余空间显示
    2. 优化部分已知问题


# 公众号
![扫码_搜索联合传播样式-白色版](https://github.com/fishzjp/FileTools/assets/105406371/49abfbc1-d46e-410c-98f1-959f2dbfe87a)

<br> 希望这次优化对你有帮助，如果还有其他需要改进的地方，请随时告知。
