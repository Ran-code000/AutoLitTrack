import yake
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

class NLPProcessor:
    def __init__(self):
        # Initialize YAKE
        self.kw_extractor = yake.KeywordExtractor(lan="en", n=3, dedupLim=0.9, top=5)
        # Initialize DistilBART-CNN with FP16
        self.model_name = "sshleifer/distilbart-cnn-12-6"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        self.model = self.model.half().to("cuda" if torch.cuda.is_available() else "cpu")

    def extract_keywords(self, text: str) -> list[str]:
        """
        Extract up to 5 keywords using YAKE.
        """
        keywords = self.kw_extractor.extract_keywords(text)
        return [kw[0] for kw in keywords]

    def generate_summary(self, text: str, max_length: int = 150) -> str:
        """
        Generate summary using DistilBART-CNN (FP16).
        """
        inputs = self.tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        summary_ids = self.model.generate(
            inputs["input_ids"],
            max_length=max_length,
            min_length=30,
            do_sample=False
        )
        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

if __name__ == "__main__":
    nlp = NLPProcessor()
    sample_text = (
        "Machine learning is a method of data analysis that automates analytical model building. "
        "It is a branch of artificial intelligence based on the idea that systems can learn "
        "from data, identify patterns and make decisions with minimal human intervention."
    )
    keywords = nlp.extract_keywords(sample_text)
    summary = nlp.generate_summary(sample_text)
    print(f"Keywords: {keywords}")
    print(f"Summary: {summary}")