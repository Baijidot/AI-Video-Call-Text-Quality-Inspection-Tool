import gradio as gr
from quality_check import start_quality_check
from report_generator import generate_simple_report, generate_html_report

# ========== 界面标题区域 ==========
title = "### AI 视频通话文本质检小工具"

# ========== 全局变量存储质检结果 ==========
current_check_result = []

# ========== 核心质检函数（按钮触发，新增 CSV 词库支持） ==========
def start_quality_check_handler(file, csv_file):
    """
    处理质检按钮点击事件
    参数：file - Gradio 上传的文本文件对象
          csv_file - Gradio 上传的 CSV 词库文件对象（可选）
    返回：上传状态文本、质检结果文本、CSV 状态文本
    """
    global current_check_result
    
    if file is None:
        return "请先上传文件", "请上传 TXT 文件后再开始质检", "未上传 CSV 词库"
    
    try:
        # 判断是否使用 CSV 词库
        csv_path = csv_file.name if csv_file is not None else None
        
        # 调用质检核心逻辑（传入 CSV 路径）
        current_check_result = start_quality_check(file.name, csv_path)
        
        # 生成 HTML 高亮报告
        report = generate_html_report(current_check_result)
        
        # 更新状态信息
        file_status = f"已上传文件：{file.name.split('/')[-1]}"
        csv_status = f"使用 CSV 词库：{csv_file.name.split('/')[-1]}" if csv_file else "使用默认 TXT 词库"
        
        return file_status, report, csv_status
    
    except Exception as e:
        csv_status = f"使用 CSV 词库：{csv_file.name.split('/')[-1]}" if csv_file else "使用默认 TXT 词库"
        return f"已上传文件：{file.name.split('/')[-1]}", f"质检出错：{str(e)}", csv_status

# ========== 文件上传处理函数 ==========
def file_upload_handler(file):
    """
    处理文本文件上传事件
    参数：file - Gradio 上传的文件对象
    返回：上传状态文本
    """
    if file is None:
        return "未上传文件"
    return f"已上传文件：{file.name.split('/')[-1]}"

# ========== 新增：CSV 词库上传处理函数 ==========
def csv_upload_handler(csv_file):
    """
    处理 CSV 词库文件上传事件
    参数：csv_file - Gradio 上传的 CSV 文件对象
    返回：CSV 上传状态文本
    """
    if csv_file is None:
        return "未上传 CSV 词库（将使用默认词库）"
    return f"已上传 CSV 词库：{csv_file.name.split('/')[-1]}"

# ========== Gradio 界面布局 ==========
with gr.Blocks(title="白芨AI 视频通话文本质检小工具") as demo:
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
            
            # ========== 新增：CSV 词库上传区 ==========
            gr.Markdown("#### 违禁词库上传区（可选）")
            gr.Markdown("*CSV 文件应包含 'Restricted words'（违规词）和 'Invalid Words'（无效词）列*")
            
            # CSV 模板下载按钮
            download_template_btn = gr.File(
                label="下载 CSV 模板",
                value="Prohibited words.CSV",
                interactive=False
            )
            
            csv_input = gr.File(
                label="可选：上传自定义违禁词列表（CSV 格式）",
                file_types=[".csv", ".CSV"]
            )
            csv_status = gr.Textbox(
                label="词库状态",
                value="未上传 CSV 词库（将使用默认词库）",
                interactive=False
            )
        
        # 右侧：结果展示区（使用 HTML 组件支持颜色高亮）
        with gr.Column(scale=2):
            gr.Markdown("#### 质检结果展示")
            result_output = gr.HTML(
                value="<p style='padding: 20px; text-align: center; color: #666;'>点击下方 \"开始质检\" 按钮，等待结果生成...</p>"
            )
    
    # 底部：开始质检按钮
    check_button = gr.Button("开始质检", variant="primary", size="lg")
    
    # ========== 事件绑定 ==========
    # 文本文件上传时更新状态
    file_input.change(
        fn=file_upload_handler,
        inputs=[file_input],
        outputs=[upload_status]
    )
    
    # ========== 新增：CSV 词库上传时更新状态 ==========
    csv_input.change(
        fn=csv_upload_handler,
        inputs=[csv_input],
        outputs=[csv_status]
    )
    
    # 点击质检按钮时执行质检（新增 CSV 参数）
    check_button.click(
        fn=start_quality_check_handler,
        inputs=[file_input, csv_input],
        outputs=[upload_status, result_output, csv_status]
    )

# ========== 启动应用 ==========
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False, inbrowser=True)
