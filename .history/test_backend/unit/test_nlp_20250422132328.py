# test_backend/unit/test_nlp.py

import pytest
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
    summary = nlp_processor.generate_summary(SAMPLE_TEXT)
    
    # Check that a summary is generated
    assert summary is not None, "Summary should not be None"
    
    # Check that the summary is a string
    assert isinstance(summary, str), "Summary should be a string"
    
    # Check that the summary has a reasonable length
    assert 30 <= len(summary.split()) <= 150, "Summary length should be between 30 and 150 words"
    
    # Check for key concepts in the summary
    assert "machine learning" in summary.lower(), "Summary should mention 'machine learning'"
    assert "artificial intelligence" in summary.lower(), "Summary should mention 'artificial intelligence'"

def test_extract_keywords_empty_input(nlp_processor):
    """
    Test keyword extraction with empty input.
    """
    keywords = nlp_processor.extract_keywords("")
    assert keywords == [], "Empty input should return an empty list"

def test_generate_summary_empty_input(nlp_processor):
    """
    Test summary generation with empty input.
    """
    summary = nlp_processor.generate_summary("")
    assert summary is None, "Empty input should return None"

def test_generate_summary_long_input(nlp_processor):
    """
    Test summary generation with a long input that exceeds the tokenizer's max length.
    """
    long_text = SAMPLE_TEXT * 10  # Create a very long text
    summary = nlp_processor.generate_summary(long_text)
    
    # Check that a summary is still generated despite truncation
    assert summary is not None, "Summary should not be None for long input"
    assert isinstance(summary, str), "Summary should be a string for long input"