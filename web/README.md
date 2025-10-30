# 🎯 Sentiment Analysis Frontend

A beautiful Streamlit web application for real-time sentiment analysis using the AWS Bedrock API.

## ✨ Features

- **Single Text Analysis** - Analyze individual messages, tweets, reviews
- **Batch Analysis** - Process multiple texts at once
- **Real-time Results** - Instant sentiment scoring with visual feedback
- **Analytics Dashboard** - Sentiment distribution charts and metrics
- **History Tracking** - Keep track of recent analyses
- **Responsive Design** - Works on desktop and mobile

## 🚀 Quick Start

1. **Install dependencies**
   ```bash
   cd frontend
   pip install -r requirements.txt
   ```

2. **Run the app**
   ```bash
   streamlit run app.py
   ```

3. **Open in browser**
   ```
   http://localhost:8501
   ```

## 📊 Screenshots

The app includes:
- Text input with real-time analysis
- Color-coded sentiment results (🟢 Positive, 🟡 Neutral, 🔴 Negative)
- Interactive pie charts showing sentiment distribution
- Recent analysis history
- Batch processing capabilities

## ⚙️ Configuration

Update `config.py` to change the API endpoint:
```python
API_ENDPOINT = "your-api-gateway-url"
```

## 🎨 Customization

The app uses:
- **Colors**: Green (positive), Yellow (neutral), Red (negative)
- **Emojis**: 😊 (positive), 😐 (neutral), 😞 (negative)
- **Layout**: Wide layout with sidebar analytics

## 🚀 Deployment

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy automatically

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### AWS EC2
```bash
# Install dependencies
pip install -r requirements.txt

# Run with external access
streamlit run app.py --server.address 0.0.0.0
```