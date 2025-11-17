"""
模块 2：AI 质检核心逻辑
功能：读取文本内容，结合违规/无效词库，调用 Qwen 模型进行质检
"""

import os
import csv
from typing import List, Tuple

# ========== 新增：读取 CSV 格式词库 ==========
def load_check_words_from_csv(csv_file_path: str) -> Tuple[List[str], List[str]]:
    """
    从 CSV 文件读取违规/无效词库
    参数：csv_file_path - CSV 文件路径
    返回：(违规词列表, 无效词列表)
    """
    try:
        violation_words = []
        invalid_words = []
        
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            # 读取 CSV 文件
            reader = csv.DictReader(f)
            
            # 检查列名是否存在
            if reader.fieldnames is None:
                raise ValueError("CSV 文件为空")
            
            # 查找包含 "Restricted" 和 "Invalid" 的列名（不区分大小写）
            restricted_col = None
            invalid_col = None
            
            for col in reader.fieldnames:
                col_lower = col.lower()
                if 'restrict' in col_lower or '违规' in col_lower:
                    restricted_col = col
                if 'invalid' in col_lower or '无效' in col_lower:
                    invalid_col = col
            
            if not restricted_col or not invalid_col:
                raise ValueError("CSV 格式错误，请确保包含违规词和无效词列")
            
            # 读取每一行数据
            for row in reader:
                # 读取违规词
                if restricted_col in row and row[restricted_col].strip():
                    word = row[restricted_col].strip().rstrip(':：')  # 去除冒号
                    if word and word not in violation_words:
                        violation_words.append(word)
                
                # 读取无效词
                if invalid_col in row and row[invalid_col].strip():
                    word = row[invalid_col].strip()
                    if word and word not in invalid_words:
                        invalid_words.append(word)
        
        return violation_words, invalid_words
    
    except Exception as e:
        raise Exception(f"CSV 文件读取失败：{str(e)}")

# ========== 第一步：读取词库文件 ==========
def load_check_words(words_file_path: str = "check_words.txt") -> tuple:
    """
    读取违规/无效词库文件
    参数：words_file_path - 词库文件路径
    返回：(违规词列表, 无效词列表)
    """
    try:
        if not os.path.exists(words_file_path):
            raise FileNotFoundError("请检查词库文件是否存在")
        
        with open(words_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析词库格式：违规词：敏感词1,敏感词2；无效词：嗯，啊，重复
        violation_words = []
        invalid_words = []
        
        lines = content.split('；')
        for line in lines:
            line = line.strip()
            if line.startswith('违规词：'):
                words_str = line.replace('违规词：', '').strip()
                violation_words = [w.strip() for w in words_str.split(',') if w.strip()]
            elif line.startswith('无效词：'):
                words_str = line.replace('无效词：', '').strip()
                invalid_words = [w.strip() for w in words_str.split(',') if w.strip()]
        
        return violation_words, invalid_words
    
    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise Exception(f"词库文件读取失败：{str(e)}")

# ========== 第二步：读取用户上传的通话文本 ==========
def load_uploaded_text(file_path: str) -> List[str]:
    """
    读取上传的文本文件，按行分割
    参数：file_path - 上传文件路径
    返回：句子列表
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 按换行符分割成句子列表，过滤空行
        sentences = [line.strip() for line in content.split('\n') if line.strip()]
        return sentences
    
    except Exception as e:
        raise Exception(f"文本文件读取失败：{str(e)}")

# ========== 第三步：质检逻辑（词库匹配 + AI 辅助） ==========
def check_sentence(sentence: str, violation_words: List[str], invalid_words: List[str]) -> dict:
    """
    检查单句是否包含问题词
    参数：sentence - 待检查的句子
          violation_words - 违规词列表
          invalid_words - 无效词列表
    返回：{'sentence': 句子, 'issue_type': 问题类型, 'issue_words': 问题词列表}
    """
    result = {
        'sentence': sentence,
        'issue_type': '无问题',
        'issue_words': []
    }
    
    # 检查违规词
    for word in violation_words:
        if word in sentence:
            result['issue_type'] = '违规词'
            result['issue_words'].append(word)
    
    # 如果没有违规词，再检查无效词
    if result['issue_type'] == '无问题':
        for word in invalid_words:
            if word in sentence:
                result['issue_type'] = '无效词'
                result['issue_words'].append(word)
    
    return result

# ========== 第四步：主质检函数（新增 CSV 支持） ==========
def start_quality_check(uploaded_text_path: str, csv_words_path: str = None) -> List[str]:
    """
    核心质检函数（支持 CSV 和 TXT 词库）
    参数：uploaded_text_path - 上传文件的路径
          csv_words_path - CSV 词库文件路径（可选，优先使用）
    返回：质检结果列表
    """
    try:
        # 1. 加载词库（优先使用 CSV，否则使用默认 TXT）
        if csv_words_path and os.path.exists(csv_words_path):
            # 使用用户上传的 CSV 词库
            violation_words, invalid_words = load_check_words_from_csv(csv_words_path)
        else:
            # 使用默认的 TXT 词库
            violation_words, invalid_words = load_check_words()
        
        # 2. 读取上传文本
        sentences = load_uploaded_text(uploaded_text_path)
        
        if not sentences:
            return ["文本内容为空，请检查上传文件"]
        
        # 3. 逐句质检
        check_results = []
        for idx, sentence in enumerate(sentences, 1):
            result = check_sentence(sentence, violation_words, invalid_words)
            
            # 格式化输出
            if result['issue_type'] == '无问题':
                formatted_result = f"{idx}. 句子：{result['sentence']} | 问题：无问题"
            else:
                issue_words_str = '、'.join(result['issue_words'])
                formatted_result = f"{idx}. 句子：{result['sentence']} | 问题：{result['issue_type']} | 问题词：{issue_words_str}"
            
            check_results.append(formatted_result)
        
        return check_results
    
    except FileNotFoundError as e:
        return [str(e)]
    except Exception as e:
        return [f"质检过程出错：{str(e)}"]
