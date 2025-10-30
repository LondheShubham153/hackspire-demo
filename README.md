# 🎯 AI Sentiment Analysis API

A serverless sentiment analysis API built with AWS CDK, Lambda, and Bedrock. Analyzes text sentiment using Meta's Llama 3 8B model and returns structured results perfect for frontend integration.

## 🚀 Features

- **Real-time Sentiment Analysis** - Analyze tweets, comments, reviews, and feedback
- **AI-Powered** - Uses Meta Llama 3 8B Instruct model via AWS Bedrock
- **Serverless Architecture** - AWS Lambda + API Gateway for scalability
- **Frontend-Ready** - Clean JSON responses with numeric scores and labels
- **CORS Enabled** - Ready for web application integration
- **Error Handling** - Comprehensive validation and error responses

## 📊 Sentiment Scoring

| Score | Label | Description |
|-------|-------|-------------|
| `1` | `positive` | Positive sentiment detected |
| `0` | `neutral` | Neutral or mixed sentiment |
| `-1` | `negative` | Negative sentiment detected |

## 🏗️ Architecture

```
Frontend → API Gateway → Lambda Function → AWS Bedrock (Llama 3) → Response
```

## 🛠️ Tech Stack

- **Infrastructure**: AWS CDK (Python)
- **Compute**: AWS Lambda (Python 3.9)
- **API**: Amazon API Gateway
- **AI Model**: Meta Llama 3 8B Instruct (AWS Bedrock)
- **Permissions**: AWS IAM

## 📡 API Endpoint

**Base URL**: `https://glb2onnqm8.execute-api.us-west-2.amazonaws.com/prod/`

### POST /
Analyze sentiment of a text message.

**Request:**
```json
{
  "message": "I love this product! It works amazingly well!"
}
```

**Response:**
```json
{
  "message": "I love this product! It works amazingly well!",
  "sentiment": {
    "score": 1,
    "label": "positive"
  }
}
```

**Error Response:**
```json
{
  "error": "Message cannot be empty"
}
```

## 🧪 Testing Examples

### Positive Sentiment
```bash
curl -X POST https://glb2onnqm8.execute-api.us-west-2.amazonaws.com/prod/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Amazing service! Highly recommend!"}'
```

### Negative Sentiment
```bash
curl -X POST https://glb2onnqm8.execute-api.us-west-2.amazonaws.com/prod/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Terrible experience. Very disappointed."}'
```

### Neutral Sentiment
```bash
curl -X POST https://glb2onnqm8.execute-api.us-west-2.amazonaws.com/prod/ \
  -H "Content-Type: application/json" \
  -d '{"message": "The weather is cloudy today."}'
```

## 🚀 Quick Start

### Prerequisites
- AWS CLI configured
- Node.js 18+ and npm
- Python 3.9+
- AWS CDK CLI

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sentiment-analysis-api
   ```

2. **Install dependencies**
   ```bash
   npm install -g aws-cdk
   pip install -r requirements.txt
   ```

3. **Bootstrap CDK (first time only)**
   ```bash
   cdk bootstrap
   ```

4. **Deploy the stack**
   ```bash
   cdk deploy
   ```

5. **Test the API**
   ```bash
   curl -X POST <your-api-url> \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello world!"}'
   ```

## 📁 Project Structure

```
├── lambda/
│   └── sentiment_analysis.py    # Lambda function code
├── workshop/
│   ├── __init__.py
│   └── workshop_stack.py        # CDK infrastructure
├── frontend/                    # Streamlit web app
│   ├── app.py                   # Main Streamlit app
│   ├── config.py                # API configuration
│   ├── requirements.txt         # Frontend dependencies
│   └── README.md                # Frontend documentation
├── tests/                       # Unit tests
├── app.py                       # CDK app entry point
├── cdk.json                     # CDK configuration
├── requirements.txt             # CDK dependencies
├── README.md                    # This file
└── .gitignore                   # Git ignore rules
```

## 🔧 Development

### Local Testing
```bash
# Synthesize CloudFormation template
cdk synth

# Run tests
python -m pytest tests/

# Deploy changes
cdk deploy
```

### Environment Variables
The Lambda function uses these AWS services:
- `AWS_REGION` - Automatically set by Lambda
- Bedrock model: `meta.llama3-8b-instruct-v1:0`

## 🌐 Frontend Integration

### JavaScript/React Example
```javascript
const analyzeSentiment = async (message) => {
  try {
    const response = await fetch('https://glb2onnqm8.execute-api.us-west-2.amazonaws.com/prod/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message })
    });
    
    const result = await response.json();
    
    // Use result.sentiment.score (1, 0, -1)
    // Use result.sentiment.label ("positive", "neutral", "negative")
    
    return result;
  } catch (error) {
    console.error('Sentiment analysis failed:', error);
  }
};
```

### Python Example
```python
import requests

def analyze_sentiment(message):
    url = "https://glb2onnqm8.execute-api.us-west-2.amazonaws.com/prod/"
    payload = {"message": message}
    
    response = requests.post(url, json=payload)
    return response.json()

# Usage
result = analyze_sentiment("I love this!")
print(f"Sentiment: {result['sentiment']['label']} ({result['sentiment']['score']})")
```

## 🔒 Security & Permissions

- **IAM Roles**: Least privilege access to Bedrock models
- **CORS**: Enabled for web applications
- **Input Validation**: Message length and content validation
- **Error Handling**: No sensitive information in error responses

## 💰 Cost Optimization

- **Serverless**: Pay only for requests processed
- **Efficient Model**: Uses Llama 3 8B (no marketplace fees)
- **Short Timeout**: 30-second Lambda timeout
- **Minimal Tokens**: Optimized prompts for quick responses

## 🖥️ Frontend Application

A beautiful Streamlit web interface is included:

```bash
# Run the frontend
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

**Frontend Features:**
- 🎯 Single text analysis
- 📊 Batch processing
- 📈 Real-time analytics
- 📱 Responsive design
- 🎨 Color-coded results
- 📝 Analysis history

## 🚧 Roadmap

- [x] Frontend web application
- [x] Batch processing endpoint
- [ ] Confidence scores
- [ ] Multi-language support
- [ ] Caching layer
- [ ] Rate limiting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Create an issue in this repository
- Check AWS Bedrock documentation
- Review CDK documentation

---

**Built with ❤️ using AWS CDK and Meta Llama 3**