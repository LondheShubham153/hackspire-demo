"""
Unit tests for utility functions
"""
import pytest
from utils import sanitize_text, validate_message, extract_sentiment_score

class TestSanitizeText:
    """Test text sanitization"""
    
    def test_basic_sanitization(self):
        """Test basic text sanitization"""
        text = "  Hello World!  "
        result = sanitize_text(text)
        assert result == "Hello World!"
    
    def test_html_decode(self):
        """Test HTML entity decoding"""
        text = "&lt;script&gt;alert('xss')&lt;/script&gt;"
        result = sanitize_text(text)
        assert result == "<script>alert('xss')</script>"
    
    def test_excessive_whitespace(self):
        """Test excessive whitespace removal"""
        text = "Hello    World\n\n\nTest"
        result = sanitize_text(text)
        assert result == "Hello World Test"
    
    def test_empty_text(self):
        """Test empty text handling"""
        assert sanitize_text("") == ""
        assert sanitize_text(None) == ""
    
    def test_control_characters(self):
        """Test control character removal"""
        text = "Hello\x00\x01World"
        result = sanitize_text(text)
        assert result == "HelloWorld"

class TestValidateMessage:
    """Test message validation"""
    
    def test_valid_message(self):
        """Test valid message"""
        is_valid, error = validate_message("Hello World!")
        assert is_valid is True
        assert error is None
    
    def test_empty_message(self):
        """Test empty message"""
        is_valid, error = validate_message("")
        assert is_valid is False
        assert "required" in error.lower()
    
    def test_none_message(self):
        """Test None message"""
        is_valid, error = validate_message(None)
        assert is_valid is False
        assert "required" in error.lower()
    
    def test_whitespace_only_message(self):
        """Test whitespace-only message"""
        is_valid, error = validate_message("   \n\t   ")
        assert is_valid is False
        assert "empty" in error.lower()
    
    def test_too_long_message(self):
        """Test message too long"""
        long_message = "x" * 6000  # Exceeds MAX_MESSAGE_LENGTH
        is_valid, error = validate_message(long_message)
        assert is_valid is False
        assert "characters" in error.lower()

class TestExtractSentimentScore:
    """Test sentiment score extraction"""
    
    def test_positive_sentiment(self):
        """Test positive sentiment extraction"""
        response = "The sentiment score is: 1"
        score = extract_sentiment_score(response)
        assert score == 1
    
    def test_negative_sentiment(self):
        """Test negative sentiment extraction"""
        response = "Analysis result: -1"
        score = extract_sentiment_score(response)
        assert score == -1
    
    def test_neutral_sentiment(self):
        """Test neutral sentiment extraction"""
        response = "Sentiment: 0"
        score = extract_sentiment_score(response)
        assert score == 0
    
    def test_no_valid_score(self):
        """Test fallback to neutral when no valid score"""
        response = "No clear sentiment detected"
        score = extract_sentiment_score(response)
        assert score == 0
    
    def test_invalid_score(self):
        """Test invalid score fallback"""
        response = "Score: 5"  # Invalid score
        score = extract_sentiment_score(response)
        assert score == 0