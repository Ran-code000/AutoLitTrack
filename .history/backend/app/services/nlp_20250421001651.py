import yake
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
from typing import List, Optional

class NLPProcessor:
    """自然语言处理处理器，集成关键词提取和文本摘要功能"""
    
    def __init__(self, model_name: str = "sshleifer/distilbart-cnn-12-6"):
        """
        初始化NLP处理组件
        :param model_name: 预训练模型名称，默认使用DistilBART-CNN
        """
        # 1. 初始化YAKE关键词提取器（无监督学习）
        self.kw_extractor = yake.KeywordExtractor(
            lan="en",          # 处理英文文本
            n=3,               # 关键词最大3个单词组合
            dedupLim=0.9,      # 相似度超过90%的关键词去重
            top=5,             # 返回前5个关键词
            features=None      # 不使用额外特征
        )
        
        # 2. 初始化文本摘要模型（默认使用蒸馏版BART）
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        
        # 3. 设备配置与模型优化
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.half().to(self.device)  # FP16量化加速
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        提取文本关键词
        :param text: 输入文本（如论文摘要）
        :return: 关键词列表（按重要性排序），出错时返回空列表
        """
        try:
            keywords = self.kw_extractor.extract_keywords(text)
            return [kw[0] for kw in keywords]  # 提取关键词文本（忽略分数）
        except Exception as e:
            print(f"[ERROR] 关键词提取失败: {e}")
            return []
    
    def generate_summary(self, text: str, max_length: int = 150, min_length: int = 30) -> Optional[str]:
        """
        生成文本摘要
        :param text: 输入文本（如论文摘要）
        :param max_length: 摘要最大长度
        :param min_length: 摘要最小长度
        :return: 生成的摘要文本，出错时返回None
        """
        try:
            # 文本编码（自动截断长文本）
            inputs = self.tokenizer(
                text,
                return_tensors="pt",  # 返回PyTorch张量
                max_length=1024,      # 模型最大输入长度
                truncation=True       # 启用自动截断
            )
            
            # 将输入数据移动到模型所在设备
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # 生成摘要（使用beam search提高质量）
            summary_ids = self.model.generate(
                inputs["input_ids"],
                max_length=max_length,
                min_length=min_length,
                do_sample=False,     # 不使用随机采样
                num_beams=4,         # beam search宽度
                early_stopping=True   # 提前终止生成
            )
            
            # 解码为可读文本
            return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        except Exception as e:
            print(f"[ERROR] 摘要生成失败: {e}")
            return None

if __name__ == "__main__":
    """测试用例"""
    # 初始化处理器（自动检测GPU）
    nlp = NLPProcessor()
    
    # 示例文本（机器学习简介）
    sample_text = (
        "Machine learning is a method of data analysis that automates analytical model building. "
        "It is a branch of artificial intelligence based on the idea that systems can learn "
        "from data, identify patterns and make decisions with minimal human intervention."
    )
    
    # 测试关键词提取
    keywords = nlp.extract_keywords(sample_text)
    print(f"提取的关键词: {keywords}")
    
    # 测试摘要生成（带长度控制）
    summary = nlp.generate_summary(
        sample_text,
        max_length=100,  # 限制摘要长度
        min_length=20    # 保证摘要完整性
    )
    print(f"生成的摘要: {summary}")