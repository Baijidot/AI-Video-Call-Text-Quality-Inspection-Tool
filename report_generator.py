"""
模块 3：简易质检报告生成
功能：统计质检结果，生成格式化报告
"""

from typing import List

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
