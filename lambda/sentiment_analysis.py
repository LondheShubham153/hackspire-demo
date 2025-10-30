import json
import boto3
from typing import Dict, Any, Optional
from config import Config
from utils import sanitize_text, validate_message, extract_sentiment_score

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Sentiment Analysis Lambda function with health check support
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    try:
        # Handle health check
        if event.get('httpMethod') == 'GET' and event.get('path') == '/health':
            return create_response(200, {'status': 'healthy', 'service': 'sentiment-analysis'})
        
        # Handle OPTIONS for CORS
        if event.get('httpMethod') == 'OPTIONS':
            return create_response(200, {'message': 'CORS preflight'})
        
        # Get message from request
        message = extract_message_from_event(event)
        if not message:
            return create_error_response(400, 'Message is required')
        
        # Sanitize and validate message
        sanitized_message = sanitize_text(message)
        is_valid, error_msg = validate_message(sanitized_message)
        
        if not is_valid:
            return create_error_response(400, error_msg)
        
        # Analyze sentiment
        sentiment_result = analyze_sentiment(sanitized_message)
        
        return create_response(200, {
            'message': sanitized_message,
            'sentiment': sentiment_result
        })
        
    except Exception as e:
        return create_error_response(500, f'Internal server error: {str(e)}')

def extract_message_from_event(event: Dict[str, Any]) -> Optional[str]:
    """
    Extract message from API Gateway event
    
    Args:
        event: API Gateway event
        
    Returns:
        Message string or None
    """
    body = event.get('body')
    if not body:
        return None
    
    try:
        parsed_body = json.loads(body)
        return parsed_body.get('message', '')
    except json.JSONDecodeError:
        return None

def analyze_sentiment(message: str) -> Dict[str, Any]:
    """
    Analyze sentiment using Bedrock
    
    Args:
        message: Sanitized message
        
    Returns:
        Sentiment analysis result
    """
    # Initialize Bedrock client
    bedrock = boto3.client('bedrock-runtime', region_name=Config.BEDROCK_REGION)
    
    # Create sentiment analysis prompt
    sentiment_prompt = Config.get_sentiment_prompt(message)
    
    # Prepare request
    request_body = {
        "prompt": sentiment_prompt,
        **Config.BEDROCK_CONFIG
    }
    
    # Call Bedrock model
    response = bedrock.invoke_model(
        modelId=Config.BEDROCK_MODEL_ID,
        body=json.dumps(request_body)
    )
    
    # Parse response
    response_body = json.loads(response['body'].read())
    ai_response = response_body['generation']
    
    # Extract sentiment score
    sentiment_score = extract_sentiment_score(ai_response)
    sentiment_label = Config.SENTIMENT_LABELS.get(sentiment_score, 'neutral')
    
    return {
        'score': sentiment_score,
        'label': sentiment_label
    }

def create_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create standardized API response
    
    Args:
        status_code: HTTP status code
        body: Response body
        
    Returns:
        API Gateway response
    """
    return {
        'statusCode': status_code,
        'headers': Config.CORS_HEADERS,
        'body': json.dumps(body)
    }

def create_error_response(status_code: int, error_message: str) -> Dict[str, Any]:
    """
    Create standardized error response
    
    Args:
        status_code: HTTP status code
        error_message: Error message
        
    Returns:
        API Gateway error response
    """
    return create_response(status_code, {'error': error_message})