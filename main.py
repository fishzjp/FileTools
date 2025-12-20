"""主入口文件"""
from filetools.config.logger import logger
from filetools.ui.interface import create_interface


def main():
    """主函数：启动Gradio Web应用"""
    logger.info("启动文件大小生成工具")
    app = create_interface()
    logger.info("Gradio 界面已创建，正在启动服务器...")
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)


if __name__ == '__main__':
    main()
