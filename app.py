import gradio as gr
from quality_check import start_quality_check
from report_generator import generate_simple_report

# ========== 界面标题区域 ==========
title = "### AI 视频通话文本质检小工具"

# ========== 全局变量存储质检结果 ==========
current_check_result = []

# ========== 核心质检函数（按钮触发） ==========
def start_quality_check_handler(file):
    """
    处理质检按钮点击事件
    参数：file - Gradio 上传的文件对象
    返回：上传状态文本、质检结果文本
    """
    global current_check_result
    
    if file is None:
        return "请先上传文件", "请上传 TXT 文件后再开始质检"
    
    try:
        # 调用质检核心逻辑
        current_check_result = start_quality_check(file.name)
        
        # 生成简易报告
        report = generate_simple_report(current_check_result)
        
        return f"已上传文件：{file.name.split('/')[-1]}", report
    
    except Exception as e:
        return f"已上传文件：{file.name.split('/')[-1]}", f"质检出错：{str(e)}"

# ========== 文件上传处理函数 ==========
def file_upload_handler(file):
    """
    处理文件上传事件
    参数：file - Gradio 上传的文件对象
    返回：上传状态文本
    """
    if file is None:
        return "未上传文件"
    return f"已上传文件：{file.name.split('/')[-1]}"

# ========== Gradio 界面布局 ==========
with gr.Blocks() as demo:
    # 顶部标题栏
    gr.Markdown(title)
    
    # 主体区域：左右布局
    with gr.Row():
        # 左侧：文本上传区
        with gr.Column(scale=1):
            gr.Markdown("#### 文本上传区")
            file_input = gr.File(
                label="上传视频通话文本记录（TXT 格式）",
                file_types=[".txt"]
            )
            upload_status = gr.Textbox(
                label="上传状态",
                value="未上传文件",
                interactive=False
            )
        
        # 右侧：结果展示区
        with gr.Column(scale=2):
            gr.Markdown("#### 质检结果展示")
            result_output = gr.Textbox(
                label="质检结果",
                value="点击下方 \"开始质检\" 按钮，等待结果生成...",
                lines=20,
                interactive=False
            )
    
    # 底部：开始质检按钮
    check_button = gr.Button("开始质检", variant="primary", size="lg")
    
    # ========== 事件绑定 ==========
    # 文件上传时更新状态
    file_input.change(
        fn=file_upload_handler,
        inputs=[file_input],
        outputs=[upload_status]
    )
    
    # 点击质检按钮时执行质检
    check_button.click(
        fn=start_quality_check_handler,
        inputs=[file_input],
        outputs=[upload_status, result_output]
    )

# ========== 启动应用 ==========
if __name__ == "__main__":
    demo.launch()
