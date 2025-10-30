import json
import boto3
import re

def lambda_handler(event, context):
    """
    Sentiment Analysis Lambda function
    """
    try:
        # Get message from API Gateway request
        body = event.get('body')
        if body:
            body = json.loads(body)
            message = body.get('message', '')
        else:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Message is required'
                })
            }
        
        if not message.strip():
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Message cannot be empty'
                })
            }
        
        # Initialize Bedrock client
        bedrock = boto3.client('bedrock-runtime')
        
        # Create sentiment analysis prompt
        sentiment_prompt = f"""Analyze the sentiment of this message and respond with ONLY the number:
1 for positive sentiment
0 for neutral sentiment
-1 for negative sentiment

Message: "{message}"

Sentiment score:"""
        
        # Prepare request for Llama 3 8B
        request_body = {
            "prompt": sentiment_prompt,
            "max_gen_len": 10,
            "temperature": 0.1
        }
        
        # Call Llama 3 8B model
        response = bedrock.invoke_model(
            modelId='meta.llama3-8b-instruct-v1:0',
            body=json.dumps(request_body)
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        ai_response = response_body['generation'].strip()
        
        # Extract sentiment score
        sentiment_match = re.search(r'(-?[01])', ai_response)
        if sentiment_match:
            sentiment_score = int(sentiment_match.group(1))
        else:
            # Fallback sentiment analysis
            sentiment_score = 0
        
        # Map sentiment score to label
        sentiment_labels = {1: 'positive', 0: 'neutral', -1: 'negative'}
        sentiment_label = sentiment_labels.get(sentiment_score, 'neutral')
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': message,
                'sentiment': {
                    'score': sentiment_score,
                    'label': sentiment_label
                }
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }