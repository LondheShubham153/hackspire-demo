"""
Configuration settings for the sentiment analysis application
"""
import os
from typing import Dict, Any

class Config:
    """Application configuration"""
    
    # Bedrock Configuration
    BEDROCK_MODEL_ID: str = "meta.llama3-8b-instruct-v1:0"
    BEDROCK_REGION: str = os.getenv("AWS_REGION", "us-west-2")
    
    # Lambda Configuration
    LAMBDA_TIMEOUT: int = 30
    MAX_MESSAGE_LENGTH: int = 5000
    MIN_MESSAGE_LENGTH: int = 1
    
    # Sentiment Analysis Configuration
    SENTIMENT_LABELS: Dict[int, str] = {
        1: "positive",
        0: "neutral", 
        -1: "negative"
    }
    
    # API Configuration
    CORS_HEADERS: Dict[str, str] = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # Bedrock Request Configuration
    BEDROCK_CONFIG: Dict[str, Any] = {
        "max_gen_len": 10,
        "temperature": 0.1
    }
    
    @staticmethod
    def get_sentiment_prompt(message: str) -> str:
        """Generate sentiment analysis prompt"""
        return f"""Analyze the sentiment of this message and respond with ONLY the number:
1 for positive sentiment
0 for neutral sentiment
-1 for negative sentiment

Message: "{message}"

Sentiment score:"""