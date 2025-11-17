"""
模块 3：简易质检报告生成
功能：统计质检结果，生成格式化报告（支持 HTML 高亮显示）
"""

from typing import List
import re

def generate_simple_report(check_result_list: List[str]) -> str:
    """
    生成简易质检报告
    参数：check_result_list - 质检结果列表
    返回：格式化的报告字符串
    """
    # 边界情况处理
    if not check_result_list:
        return "暂无质检数据，请先上传文本"
    
    # 如果是错误信息，直接返回
    if len(check_result_list) == 1 and ("出错" in check_result_list[0] or "请检查" in check_result_list[0]):
        return check_result_list[0]
    
    # ========== 统计数据 ==========
    total_sentences = len(check_result_list)
    qualified_sentences = 0  # 合格句子数
    violation_sentences = 0  # 违规词句子数
    invalid_sentences = 0    # 无效词句子数
    
    for result in check_result_list:
        if "问题：无问题" in result:
            qualified_sentences += 1
        elif "问题：违规词" in result:
            violation_sentences += 1
        elif "问题：无效词" in result:
            invalid_sentences += 1
    
    problem_sentences = total_sentences - qualified_sentences
    
    # 计算质检通过率
    if total_sentences > 0:
        pass_rate = (qualified_sentences / total_sentences) * 100
    else:
        pass_rate = 0.0
    
    # ========== 生成报告 ==========
    report = "=" * 50 + "\n"
    report += "AI 视频通话文本质检报告\n"
    report += "=" * 50 + "\n\n"
    
    report += "【基础数据】\n"
    report += f"总句子数：{total_sentences} 句\n"
    report += f"合格句子数：{qualified_sentences} 句\n"
    report += f"问题句子数：{problem_sentences} 句\n"
    report += f"质检通过率：{pass_rate:.2f}%\n\n"
    
    report += "【问题类型分布】\n"
    report += f"违规词问题：{violation_sentences} 句\n"
    report += f"无效词问题：{invalid_sentences} 句\n\n"
    
    report += "【详细问题列表】\n"
    report += "-" * 50 + "\n"
    for result in check_result_list:
        report += result + "\n"
    
    report += "=" * 50 + "\n"
    
    return report

def generate_html_report(check_result_list: List[str]) -> str:
    """
    生成带颜色高亮的 HTML 质检报告
    参数：check_result_list - 质检结果列表
    返回：HTML 格式的报告字符串
    """
    # 边界情况处理
    if not check_result_list:
        return "<p>暂无质检数据，请先上传文本</p>"
    
    # 如果是错误信息，直接返回
    if len(check_result_list) == 1 and ("出错" in check_result_list[0] or "请检查" in check_result_list[0]):
        return f"<p>{check_result_list[0]}</p>"
    
    # ========== 统计数据 ==========
    total_sentences = len(check_result_list)
    qualified_sentences = 0
    violation_sentences = 0
    invalid_sentences = 0
    
    for result in check_result_list:
        if "问题：无问题" in result:
            qualified_sentences += 1
        elif "问题：违规词" in result:
            violation_sentences += 1
        elif "问题：无效词" in result:
            invalid_sentences += 1
    
    problem_sentences = total_sentences - qualified_sentences
    pass_rate = (qualified_sentences / total_sentences) * 100 if total_sentences > 0 else 0.0
    
    # ========== 生成 HTML 报告 ==========
    # 确定通过率颜色
    if pass_rate >= 80:
        rate_color = "#4CAF50"
    elif pass_rate >= 60:
        rate_color = "#ff9800"
    else:
        rate_color = "#f44336"
    
    html = f"""
    <style>
        .report-container {{ font-family: Arial, sans-serif; padding: 10px; }}
        .report-title {{ font-size: 18px; font-weight: bold; color: #333; border-bottom: 2px solid #333; padding-bottom: 5px; margin-bottom: 15px; }}
        .stats-section {{ background: #f5f5f5; padding: 10px; border-radius: 5px; margin-bottom: 15px; }}
        .stats-item {{ margin: 5px 0; }}
        .detail-section {{ margin-top: 15px; }}
        .sentence-item {{ padding: 8px; margin: 5px 0; border-left: 3px solid #ddd; background: #fafafa; }}
        .sentence-ok {{ border-left-color: #4CAF50; background: #f1f8f4; }}
        .sentence-violation {{ border-left-color: #f44336; background: #ffebee; }}
        .sentence-invalid {{ border-left-color: #ff9800; background: #fff3e0; }}
        .highlight-violation {{ background: #ff5252; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; }}
        .highlight-invalid {{ background: #ffa726; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold; }}
        .problem-label {{ font-weight: bold; }}
        .label-ok {{ color: #4CAF50; }}
        .label-violation {{ color: #f44336; }}
        .label-invalid {{ color: #ff9800; }}
    </style>
    <div class="report-container">
        <div class="report-title">📊 AI 视频通话文本质检报告</div>
        
        <div class="stats-section">
            <div class="stats-item"><strong>总句子数：</strong>{total_sentences} 句</div>
            <div class="stats-item"><strong>合格句子数：</strong><span style="color: #4CAF50;">{qualified_sentences}</span> 句</div>
            <div class="stats-item"><strong>问题句子数：</strong><span style="color: #f44336;">{problem_sentences}</span> 句</div>
            <div class="stats-item"><strong>质检通过率：</strong><span style="color: {rate_color}; font-weight: bold;">{pass_rate:.2f}%</span></div>
            <div class="stats-item" style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #ddd;">
                <strong>问题类型分布：</strong>
                <span style="color: #f44336;">违规词 {violation_sentences} 句</span> | 
                <span style="color: #ff9800;">无效词 {invalid_sentences} 句</span>
            </div>
        </div>
        
        <div class="detail-section">
            <div style="font-weight: bold; margin-bottom: 10px;">📝 详细问题列表：</div>
    """
    
    # ========== 处理每一条结果，添加高亮 ==========
    for result in check_result_list:
        # 解析结果字符串
        if "问题：无问题" in result:
            sentence_class = "sentence-ok"
            label_class = "label-ok"
            label_text = "✓ 无问题"
            # 提取句子内容
            match = re.search(r'句子：(.+?) \| 问题：', result)
            sentence_text = match.group(1) if match else result
            problem_words = ""
        elif "问题：违规词" in result:
            sentence_class = "sentence-violation"
            label_class = "label-violation"
            label_text = "✗ 违规词"
            # 提取句子和问题词
            match_sentence = re.search(r'句子：(.+?) \| 问题：', result)
            match_words = re.search(r'问题词：(.+?)$', result)
            sentence_text = match_sentence.group(1) if match_sentence else ""
            problem_words_list = match_words.group(1).split('、') if match_words else []
            
            # 高亮违规词
            for word in problem_words_list:
                sentence_text = sentence_text.replace(word, f'<span class="highlight-violation">{word}</span>')
            problem_words = f' | <strong>问题词：</strong>{match_words.group(1)}' if match_words else ""
        elif "问题：无效词" in result:
            sentence_class = "sentence-invalid"
            label_class = "label-invalid"
            label_text = "⚠ 无效词"
            # 提取句子和问题词
            match_sentence = re.search(r'句子：(.+?) \| 问题：', result)
            match_words = re.search(r'问题词：(.+?)$', result)
            sentence_text = match_sentence.group(1) if match_sentence else ""
            problem_words_list = match_words.group(1).split('、') if match_words else []
            
            # 高亮无效词
            for word in problem_words_list:
                sentence_text = sentence_text.replace(word, f'<span class="highlight-invalid">{word}</span>')
            problem_words = f' | <strong>问题词：</strong>{match_words.group(1)}' if match_words else ""
        else:
            sentence_class = "sentence-item"
            label_class = ""
            label_text = ""
            sentence_text = result
            problem_words = ""
        
        # 提取序号
        match_num = re.match(r'(\d+)\. ', result)
        num_text = match_num.group(1) if match_num else ""
        
        html += f"""
            <div class="{sentence_class}">
                <span style="color: #666; font-weight: bold;">{num_text}.</span> 
                {sentence_text}
                <br>
                <span class="problem-label {label_class}">{label_text}</span>{problem_words}
            </div>
        """
    
    html += """
        </div>
    </div>
    """
    
    return html
