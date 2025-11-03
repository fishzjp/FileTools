"""主入口文件"""
from ui.interface import create_interface


def main():
    """主函数：启动Gradio Web应用"""
    app = create_interface()
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)


if __name__ == '__main__':
    main()
