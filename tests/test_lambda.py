"""
Unit tests for Lambda function
"""
import json
import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add lambda directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lambda'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import sys
sys.path.append('lambda')
from sentiment_analysis import (
    extract_message_from_event,
    create_response,
    create_error_response
)

class TestExtractMessageFromEvent:
    """Test message extraction from API Gateway event"""
    
    def test_valid_event(self):
        """Test valid event with message"""
        event = {
            'body': json.dumps({'message': 'Hello World!'})
        }
        message = extract_message_from_event(event)
        assert message == 'Hello World!'
    
    def test_no_body(self):
        """Test event without body"""
        event = {}
        message = extract_message_from_event(event)
        assert message is None
    
    def test_invalid_json(self):
        """Test event with invalid JSON"""
        event = {
            'body': 'invalid json'
        }
        message = extract_message_from_event(event)
        assert message is None
    
    def test_no_message_field(self):
        """Test event without message field"""
        event = {
            'body': json.dumps({'other_field': 'value'})
        }
        message = extract_message_from_event(event)
        assert message == ''

class TestResponseCreation:
    """Test response creation functions"""
    
    def test_create_response(self):
        """Test successful response creation"""
        response = create_response(200, {'test': 'data'})
        
        assert response['statusCode'] == 200
        assert 'Content-Type' in response['headers']
        assert response['headers']['Access-Control-Allow-Origin'] == '*'
        
        body = json.loads(response['body'])
        assert body['test'] == 'data'
    
    def test_create_error_response(self):
        """Test error response creation"""
        response = create_error_response(400, 'Test error')
        
        assert response['statusCode'] == 400
        assert 'Content-Type' in response['headers']
        
        body = json.loads(response['body'])
        assert body['error'] == 'Test error'

class TestLambdaHandler:
    """Test Lambda handler function"""
    
    @patch('sentiment_analysis.boto3.client')
    def test_health_check(self, mock_boto):
        """Test health check endpoint"""
        from sentiment_analysis import lambda_handler
        
        event = {
            'httpMethod': 'GET',
            'path': '/health'
        }
        
        response = lambda_handler(event, {})
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['status'] == 'healthy'
        assert body['service'] == 'sentiment-analysis'
    
    def test_options_request(self):
        """Test OPTIONS request for CORS"""
        from sentiment_analysis import lambda_handler
        
        event = {
            'httpMethod': 'OPTIONS'
        }
        
        response = lambda_handler(event, {})
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['message'] == 'CORS preflight'
    
    def test_missing_message(self):
        """Test request without message"""
        from sentiment_analysis import lambda_handler
        
        event = {
            'httpMethod': 'POST',
            'body': json.dumps({})
        }
        
        response = lambda_handler(event, {})
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'error' in body