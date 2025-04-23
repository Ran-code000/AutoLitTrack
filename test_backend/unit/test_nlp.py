# test_backend/unit/test_nlp.py
import pytest
import torch 
from unittest.mock import patch, MagicMock
from backend.app.services.nlp import NLPProcessor

# Sample text for testing
SAMPLE_TEXT = (
    "Machine learning is a method of data analysis that automates analytical model building. "
    "It is a branch of artificial intelligence based on the idea that systems can learn "
    "from data, identify patterns and make decisions with minimal human intervention."
)

@pytest.fixture
def nlp_processor():
    """
    Fixture to initialize NLPProcessor for testing.
    Forces CPU usage to avoid GPU-related issues in CI environments.
    """
    nlp = NLPProcessor()
    nlp.device = "cpu"  # Force CPU for testing
    nlp.model = nlp.model.to("cpu")  # Move model to CPU (remove .half() for simplicity)
    return nlp 

def test_extract_keywords(nlp_processor):
    """
    Test keyword extraction using YAKE.
    """
    keywords = nlp_processor.extract_keywords(SAMPLE_TEXT)
    print(f"Extracted keywords: {keywords}")  # Debug output

    # Check that keywords are returned as a list
    assert isinstance(keywords, list), "Keywords should be a list"
    
    # Check that some keywords are extracted
    assert len(keywords) > 0, "At least one keyword should be extracted"
    
    # Check that extracted keywords are strings
    assert all(isinstance(kw, str) for kw in keywords), "All keywords should be strings"
    
    # Check for expected keywords (based on sample text)
    expected_keywords = ["machine learning", "data analysis", "artificial intelligence"]
    assert any(kw in keywords for kw in expected_keywords), "Expected keywords not found"

def test_generate_summary(nlp_processor):
    """
    Test summary generation using DistilBART-CNN.
    """
    with patch.object(nlp_processor.model, "generate") as mock_generate:
        mock_generate.return_value = torch.tensor([[1, 2, 3]]) 
        
        with patch.object(nlp_processor.tokenizer, "decode", return_value="Mock summary"):
            summary = nlp_processor.generate_summary(SAMPLE_TEXT)
            assert summary == "Mock summary"
            mock_generate.assert_called_once()

def test_extract_keywords_empty_input(nlp_processor):
    """
    Test keyword extraction with empty input.
    """
    keywords = nlp_processor.extract_keywords("")
    assert keywords == [], "Empty input should return an empty list"

def test_extract_keywords_invalid_input():
    nlp_processor = NLPProcessor()
    keywords = nlp_processor.extract_keywords(None)
    assert keywords == []

def test_generate_summary_empty_input(nlp_processor):
    """
    Test summary generation with empty input.
    """
    summary = nlp_processor.generate_summary("")
    assert summary is None, "Empty input should return None"

def test_generate_summary_long_input(nlp_processor):
    """Test handling of long input texts"""
    long_text = SAMPLE_TEXT * 10
    
    # Create a mock tokenizer that returns valid tensors
    mock_tokenizer = MagicMock()
    mock_tokenizer.return_value = {
        "input_ids": torch.tensor([[1, 2, 3]]),
        "attention_mask": torch.tensor([[1, 1, 1]])
    }
    
    # Replace the actual tokenizer call
    with patch.object(nlp_processor, 'tokenizer', mock_tokenizer):
        result = nlp_processor.generate_summary(long_text)
        assert result is not None
        
        # Verify tokenizer was called with correct parameters
        args, kwargs = mock_tokenizer.call_args
        assert args[0] == long_text
        assert kwargs["max_length"] == 1024
        assert kwargs["truncation"] is True
        assert kwargs["return_tensors"] == "pt"