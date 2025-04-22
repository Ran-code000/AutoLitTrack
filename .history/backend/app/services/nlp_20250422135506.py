import yake
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
from typing import List, Optional

class NLPProcessor:
    def __init__(self, model_name: str = "sshleifer/distilbart-cnn-12-6"):
        """
        Initialize YAKE for keyword extraction and DistilBART-CNN for summarization.
        Uses FP16 quantization for efficiency.
        """
        # Initialize YAKE
        self.kw_extractor = yake.KeywordExtractor(
            lan="en",          # Language: English
            n=2,               # Maximum n-gram size
            dedupLim=0.9,      # Deduplication threshold
            top=5,             # Number of keywords
            features=None 
        )
        
        # Initialize DistilBART-CNN
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        
        # Use FP16 quantization and move to GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.half().to(self.device)
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from text using YAKE.
        Args:
            text: Input text (e.g., paper abstract).
        Returns:
            List of extracted keywords.
        """
        try:
            keywords = self.kw_extractor.extract_keywords(text)
            return [kw[0] for kw in keywords]
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return []
    
    def generate_summary(self, text: str, max_length: int = 150, min_length: int = 30) -> Optional[str]:
        """
        Generate a summary using DistilBART-CNN (FP16).
        Args:
            text: Input text (e.g., paper abstract).
            max_length: Maximum length of the summary.
            min_length: Minimum length of the summary.
        Returns:
            Generated summary or None if an error occurs.
        """
        try:
            text = text.strip()
            if not text:
                return None
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                max_length=1024,
                truncation=True
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            summary_ids = self.model.generate(
                inputs["input_ids"],
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                num_beams=4,
                early_stopping=True
            )
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary
        except Exception as e:
            print(f"Error generating summary: {e}")
            return None

if __name__ == "__main__":
    # Test the NLPProcessor
    nlp = NLPProcessor()
    sample_text = (
        "Machine learning is a method of data analysis that automates analytical model building. "
        "It is a branch of artificial intelligence based on the idea that systems can learn "
        "from data, identify patterns and make decisions with minimal human intervention."
    )
    
    # Test keyword extraction
    keywords = nlp.extract_keywords(sample_text)
    print(f"Keywords: {keywords}")
    
    # Test summary generation
    summary = nlp.generate_summary(sample_text)
    print(f"Summary: {summary}")