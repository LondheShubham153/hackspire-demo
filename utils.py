"""
Utility functions for sentiment analysis
"""
import re
import html
from typing import Tuple, Optional
from config import Config

def sanitize_text(text: str) -> str:
    """
    Sanitize input text by removing harmful content and normalizing
    
    Args:
        text: Raw input text
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # HTML decode
    text = html.unescape(text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove control characters except newlines and tabs
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

def validate_message(message: str) -> Tuple[bool, Optional[str]]:
    """
    Validate message input
    
    Args:
        message: Input message to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not message:
        return False, "Message is required"
    
    sanitized = sanitize_text(message)
    
    if not sanitized:
        return False, "Message cannot be empty"
    
    if len(sanitized) < Config.MIN_MESSAGE_LENGTH:
        return False, f"Message must be at least {Config.MIN_MESSAGE_LENGTH} character(s)"
    
    if len(sanitized) > Config.MAX_MESSAGE_LENGTH:
        return False, f"Message must be less than {Config.MAX_MESSAGE_LENGTH} characters"
    
    return True, None

def extract_sentiment_score(ai_response: str) -> int:
    """
    Extract sentiment score from AI response
    
    Args:
        ai_response: Raw AI response
        
    Returns:
        Sentiment score (-1, 0, or 1)
    """
    # Extract sentiment score using regex
    sentiment_match = re.search(r'(-?[01])', ai_response.strip())
    
    if sentiment_match:
        score = int(sentiment_match.group(1))
        # Ensure score is valid
        if score in [-1, 0, 1]:
            return score
    
    # Fallback to neutral if no valid score found
    return 0