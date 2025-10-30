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
│   ├── cdk.json           # CDK configuration
│   └── __init__.py        # Python package marker
├── services/               # Microservices
│   └── sentiment/         # Sentiment analysis service
│       ├── config.py      # Service configuration
│       ├── sentiment_analysis.py # Lambda handler
│       └── utils.py       # Utility functions
├── web/                   # Web application
│   ├── app.py            # Streamlit application
│   ├── config.py         # Web app configuration
│   ├── requirements.txt  # Web dependencies
│   ├── sentiment_history.pkl  # Persistent data (auto-generated)
│   └── sentiment_history.json # JSON backup (auto-generated)
├── .gitignore            # Git ignore patterns
├── CHANGELOG.md          # Version history
├── LICENSE              # MIT License
├── README.md           # This file
└── requirements.txt    # Root dependencies
```

## 🚀 Features

### Core Functionality
- **Real-time Sentiment Analysis**: Powered by Meta Llama 3 8B via AWS Bedrock
- **Serverless Architecture**: Scalable AWS Lambda backend with API Gateway
- **Smart Caching**: Optimized performance with request caching (5-minute TTL)
- **Health Monitoring**: API health checks and status indicators

### Web Interface
- **Modern UI**: Interactive Streamlit dashboard with gradient themes
- **Analytics Dashboard**: Real-time pie charts and trend analysis
- **Data Persistence**: Automatic save/load with pickle and JSON backup
- **Manual Controls**: Refresh, export, and clear history with confirmation
- **Responsive Design**: Mobile-friendly interface with emojis and colors

### Data Management
- **Persistent Storage**: Local file-based storage with auto-backup
- **Export Capabilities**: CSV download with timestamps
- **History Tracking**: Complete analysis history with metadata
- **Data Recovery**: Dual format storage (pickle + JSON) for reliability

## 🛠️ Prerequisites

- AWS CLI configured with appropriate permissions
- Node.js 18+ (for CDK)
- Python 3.9+
- AWS CDK v2 installed (`npm install -g aws-cdk`)

## 📋 Required AWS Permissions

Your AWS user/role needs the following permissions:
- **Bedrock**: Model access (specifically Meta Llama models)
- **Lambda**: Function creation, execution, and management
- **API Gateway**: REST API creation and deployment
- **IAM**: Role creation and policy attachment for Lambda
- **CloudFormation**: Stack operations for CDK deployment
- **CloudWatch**: Logging (automatically configured)

## 🔧 Installation & Deployment

### 1. Clone and Setup

```bash
git clone <repository-url>
cd workshop
pip install -r requirements.txt  # Install root dependencies
```

### 2. Deploy Infrastructure

```bash
cd infrastructure
pip install -r requirements.txt
cdk bootstrap  # Only needed once per AWS account/region
cdk deploy --require-approval never
```

**Important**: Note the API Gateway URL from the deployment output (e.g., `https://abc123.execute-api.us-west-2.amazonaws.com/prod/`)

### 3. Update Web Configuration

```bash
cd ../web
# Update config.py with your API Gateway URL
echo 'API_ENDPOINT = "https://YOUR-API-ID.execute-api.REGION.amazonaws.com/prod/"' > config.py
```

### 4. Run Web Application

```bash
pip install -r requirements.txt
streamlit run app.py --server.port 8501
```

The application will be available at `http://localhost:8501`

## 🧪 Testing

### Test API Endpoints

```bash
# Health check
curl -X GET "https://YOUR-API-ID.execute-api.REGION.amazonaws.com/prod/health"

# Positive sentiment
curl -X POST "https://YOUR-API-ID.execute-api.REGION.amazonaws.com/prod/" \
  -H "Content-Type: application/json" \
  -d '{"message": "I absolutely love this amazing product!"}'

# Negative sentiment  
curl -X POST "https://YOUR-API-ID.execute-api.REGION.amazonaws.com/prod/" \
  -H "Content-Type: application/json" \
  -d '{"message": "This is terrible and I hate it."}'

# Neutral sentiment
curl -X POST "https://YOUR-API-ID.execute-api.REGION.amazonaws.com/prod/" \
  -H "Content-Type: application/json" \
  -d '{"message": "The weather is cloudy today."}'
```

### Expected Responses

**Health Check:**
```json
{"status": "healthy", "service": "sentiment-analysis"}
```

**Sentiment Analysis:**
```json
{
  "message": "I absolutely love this amazing product!",
  "sentiment": {
    "score": 1,
    "label": "positive"
  }
}
```

## 📊 Configuration

### Service Configuration (`services/sentiment/config.py`)

```python
BEDROCK_MODEL_ID = "meta.llama3-8b-instruct-v1:0"  # Model identifier
BEDROCK_REGION = "us-west-2"                        # AWS region
MAX_MESSAGE_LENGTH = 5000                           # Input limit
MIN_MESSAGE_LENGTH = 1                              # Minimum input
LAMBDA_TIMEOUT = 30                                 # Function timeout
```

### Web Configuration (`web/config.py`)

```python
API_ENDPOINT = "https://YOUR-API-ID.execute-api.REGION.amazonaws.com/prod/"
```

## 🎨 Web Interface Features

### Main Dashboard
- **Text Analysis**: Large text area with real-time sentiment analysis
- **Visual Feedback**: Color-coded results with emojis and gradients
- **API Status**: Live health monitoring with connection indicators

### Analytics Sidebar
- **Sentiment Distribution**: Interactive pie chart with color coding
- **Statistics**: Total analyzed, positive/negative/neutral rates
- **Trend Analysis**: Time-series chart showing sentiment over time
- **Data Status**: File size, modification time, record count

### History Management
- **Recent History**: Last 5 analyses with timestamps and previews
- **Manual Refresh**: Reload data from persistent storage
- **CSV Export**: Download complete history with timestamps
- **Clear History**: Safe deletion with confirmation dialog

### Data Persistence
- **Auto-save**: Every analysis automatically saved to disk
- **Dual Format**: Pickle (binary) + JSON (human-readable) backup
- **Cross-session**: Data persists across browser refreshes and restarts
- **Error Recovery**: Graceful handling of corrupted files

## 🔍 Sentiment Scoring

| Score | Label | Color | Emoji | Description |
|-------|-------|-------|-------|-------------|
| 1 | Positive | 🟢 Green | 😊 | Happy, satisfied, enthusiastic |
| 0 | Neutral | 🟡 Yellow | 😐 | Factual, balanced, indifferent |
| -1 | Negative | 🔴 Red | 😞 | Unhappy, critical, disappointed |

## 🚨 Troubleshooting

### Common Issues

1. **Bedrock Access Denied**
   ```
   Error: AccessDeniedException
   ```
   - **Solution**: Enable Bedrock access in AWS Console → Bedrock → Model access
   - **Check**: IAM permissions for `bedrock:InvokeModel`

2. **Lambda Timeout**
   ```
   Error: Task timed out after 30.00 seconds
   ```
   - **Solution**: Increase timeout in `infrastructure/backend_stack.py`
   - **Check**: Bedrock service availability in your region

3. **API Gateway CORS Issues**
   ```
   Error: CORS policy blocked
   ```
   - **Solution**: CORS headers configured in `services/sentiment/config.py`
   - **Check**: Browser developer tools for specific CORS errors

4. **Web App Connection Errors**
   ```
   Error: Connection error - please check your internet
   ```
   - **Solution**: Verify API endpoint URL in `web/config.py`
   - **Check**: API Gateway deployment status in AWS Console

5. **Data Persistence Issues**
   ```
   AttributeError: 'NoneType' object has no attribute 'strftime'
   ```
   - **Solution**: Fixed in latest version with null checks
   - **Check**: File permissions in web directory

### Debugging Steps

1. **Check API Health**: Visit `/health` endpoint directly
2. **Verify Logs**: CloudWatch Logs for Lambda function
3. **Test Locally**: Use curl commands to test API
4. **Browser Console**: Check for JavaScript errors
5. **File Permissions**: Ensure web directory is writable

## 🧹 Cleanup

To avoid AWS charges, clean up all resources:

```bash
cd infrastructure
cdk destroy

# Confirm deletion when prompted
# This will remove:
# - Lambda function
# - API Gateway
# - IAM roles and policies
# - CloudWatch log groups
```

## 📝 Development Notes

### Technical Details
- **Runtime**: Python 3.9 with AWS Lambda
- **Model**: Meta Llama 3 8B Instruct via Bedrock
- **Temperature**: 0.1 (low for consistent results)
- **Max Tokens**: 10 (single number response)
- **Caching**: 5-minute TTL on API responses

### Security Features
- **Input Sanitization**: HTML entity decoding and control character removal
- **Length Validation**: Min/max message length enforcement
- **Error Handling**: Graceful degradation with user-friendly messages
- **CORS Configuration**: Proper cross-origin resource sharing setup

### Performance Optimizations
- **Smart Caching**: Streamlit cache for repeated API calls
- **Efficient Parsing**: Regex-based sentiment score extraction
- **Minimal Payload**: Optimized request/response sizes
- **Connection Pooling**: Reused HTTP connections

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests (if available)
python -m pytest

# Format code
black .

# Lint code
flake8 .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AWS Bedrock Team** - Foundation model access and infrastructure
- **Meta AI** - Llama 3 8B Instruct model
- **Streamlit Team** - Excellent web framework for Python
- **AWS CDK Team** - Infrastructure as Code capabilities
- **Open Source Community** - Various libraries and tools used

---

**Built with ❤️ using AWS Bedrock, Streamlit, and modern serverless architecture**