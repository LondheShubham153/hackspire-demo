# 🎯 AI Sentiment Analysis Workshop

A complete serverless sentiment analysis application built with AWS Bedrock, Lambda, API Gateway, and Streamlit.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │───▶│   API Gateway   │───▶│   AWS Lambda    │───▶│   AWS Bedrock   │
│   Web App       │    │                 │    │                 │    │  (Llama 3 8B)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
workshop/
├── infrastructure/          # CDK Infrastructure as Code
│   ├── app.py              # CDK App entry point
│   ├── backend_stack.py    # CDK Stack definition
│   ├── requirements.txt    # CDK dependencies
│   └── cdk.json           # CDK configuration
├── services/               # Microservices
│   └── sentiment/         # Sentiment analysis service
│       ├── config.py      # Service configuration
│       ├── sentiment_analysis.py # Lambda handler
│       └── utils.py       # Utility functions
├── web/                   # Web application
│   ├── app.py            # Streamlit application
│   ├── config.py         # Web app configuration
│   └── requirements.txt  # Web dependencies
└── README.md             # This file
```

## 🚀 Features

- **Real-time Sentiment Analysis**: Powered by Meta Llama 3 8B via AWS Bedrock
- **Modern Web Interface**: Interactive Streamlit dashboard with analytics
- **Serverless Architecture**: Scalable AWS Lambda backend
- **Smart Caching**: Optimized performance with request caching
- **Data Persistence**: Analysis history with export capabilities
- **Health Monitoring**: API health checks and status indicators
- **Responsive Design**: Modern UI with gradient themes and emojis

## 🛠️ Prerequisites

- AWS CLI configured with appropriate permissions
- Node.js 18+ (for CDK)
- Python 3.9+
- AWS CDK v2 installed (`npm install -g aws-cdk`)

## 📋 Required AWS Permissions

Your AWS user/role needs the following permissions:
- Bedrock model access (specifically Meta Llama models)
- Lambda function creation and management
- API Gateway creation and management
- IAM role creation for Lambda
- CloudFormation stack operations

## 🔧 Installation & Deployment

### 1. Clone and Setup

```bash
git clone <repository-url>
cd workshop
```

### 2. Deploy Infrastructure

```bash
cd infrastructure
pip install -r requirements.txt
cdk bootstrap  # Only needed once per AWS account/region
cdk deploy --require-approval never
```

Note the API Gateway URL from the deployment output.

### 3. Update Web Configuration

```bash
cd ../web
# Update config.py with your API Gateway URL
echo 'API_ENDPOINT = "https://YOUR-API-ID.execute-api.REGION.amazonaws.com/prod/"' > config.py
```

### 4. Run Web Application

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🧪 Testing

### Test Service Directly

```bash
# Health check
curl -X GET "https://YOUR-API-ID.execute-api.REGION.amazonaws.com/prod/health"

# Sentiment analysis
curl -X POST "https://YOUR-API-ID.execute-api.REGION.amazonaws.com/prod/" \
  -H "Content-Type: application/json" \
  -d '{"message": "I love this product!"}'
```

### Expected Response

```json
{
  "message": "I love this product!",
  "sentiment": {
    "score": 1,
    "label": "positive"
  }
}
```

## 📊 Configuration

### Service Configuration (`services/sentiment/config.py`)

- **BEDROCK_MODEL_ID**: Meta Llama 3 8B model identifier
- **BEDROCK_REGION**: AWS region for Bedrock service
- **MAX_MESSAGE_LENGTH**: Maximum input text length (5000 chars)
- **LAMBDA_TIMEOUT**: Function timeout (30 seconds)

### Web Configuration (`web/config.py`)

- **API_ENDPOINT**: Your API Gateway endpoint URL

## 🎨 Web Features

- **Sentiment Analysis**: Real-time text analysis with visual feedback
- **Analytics Dashboard**: Pie charts and trend analysis
- **History Tracking**: Persistent analysis history
- **Data Export**: CSV export functionality
- **Health Monitoring**: API status indicators
- **Responsive Design**: Modern UI with custom CSS

## 🔍 Sentiment Scoring

- **Positive (1)**: 😊 Green gradient
- **Neutral (0)**: 😐 Yellow gradient  
- **Negative (-1)**: 😞 Red gradient

## 🚨 Troubleshooting

### Common Issues

1. **Bedrock Access Denied**
   - Ensure your AWS account has Bedrock access enabled
   - Check IAM permissions for Bedrock model access

2. **Lambda Timeout**
   - Increase timeout in `infrastructure/backend_stack.py`
   - Check Bedrock service availability

3. **API Gateway CORS Issues**
   - CORS headers are configured in `services/sentiment/config.py`
   - Ensure OPTIONS method is handled

4. **Web Connection Errors**
   - Verify API endpoint URL in `web/config.py`
   - Check API Gateway deployment status

### Logs and Monitoring

- **Lambda Logs**: Check CloudWatch Logs for the Lambda function
- **API Gateway Logs**: Enable logging in API Gateway console
- **Web Logs**: Check browser console for client-side errors

## 🧹 Cleanup

To avoid AWS charges, clean up resources:

```bash
cd infrastructure
cdk destroy
```

## 📝 Development Notes

- The Lambda function uses Python 3.9 runtime
- Bedrock requests are configured with low temperature (0.1) for consistent results
- Text sanitization removes HTML entities and control characters
- Response caching improves performance for repeated queries

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- AWS Bedrock team for the foundation model access
- Meta for the Llama 3 8B model
- Streamlit team for the excellent web framework
- AWS CDK team for infrastructure as code capabilities