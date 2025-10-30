import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import pickle
from typing import List, Dict, Any
from config import API_ENDPOINT

# Page config
st.set_page_config(
    page_title="AI Sentiment Analysis",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sentiment-positive {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
    }
    .sentiment-negative {
        background: linear-gradient(90deg, #cb2d3e 0%, #ef473a 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
    }
    .sentiment-neutral {
        background: linear-gradient(90deg, #f7971e 0%, #ffd200 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Data persistence file - use absolute path
try:
    DATA_FILE = os.path.join(os.path.dirname(__file__), 'sentiment_history.pkl')
except NameError:
    # Fallback for when __file__ is not available (e.g., in some deployment contexts)
    DATA_FILE = os.path.join(os.getcwd(), 'sentiment_history.pkl')

def load_history() -> List[Dict[str, Any]]:
    """Load analysis history from file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'rb') as f:
                data = pickle.load(f)
                # Convert string timestamps back to datetime objects if needed
                for item in data:
                    if isinstance(item.get('timestamp'), str):
                        item['timestamp'] = datetime.fromisoformat(item['timestamp'])
                return data
    except Exception as e:
        st.warning(f"Could not load history: {e}")
    return []

def save_history() -> None:
    """Save analysis history to file"""
    try:
        # Convert datetime objects to strings for JSON serialization
        data_to_save = []
        for item in st.session_state.history:
            item_copy = item.copy()
            if isinstance(item_copy.get('timestamp'), datetime):
                item_copy['timestamp'] = item_copy['timestamp'].isoformat()
            data_to_save.append(item_copy)
        
        with open(DATA_FILE, 'wb') as f:
            pickle.dump(st.session_state.history, f)  # Keep original datetime objects
        
        # Also save as JSON backup
        json_file = DATA_FILE.replace('.pkl', '.json')
        with open(json_file, 'w') as f:
            json.dump(data_to_save, f, indent=2)
            
    except Exception as e:
        st.error(f"Failed to save history: {e}")

def export_to_csv() -> str:
    """Export history to CSV format"""
    if not st.session_state.history:
        return ""
    df = pd.DataFrame(st.session_state.history)
    return df.to_csv(index=False)

@st.cache_data(ttl=300)
def analyze_sentiment(message: str) -> Dict[str, Any]:
    """Call the sentiment analysis API with caching"""
    try:
        response = requests.post(
            API_ENDPOINT,
            headers={'Content-Type': 'application/json'},
            json={'message': message},
            timeout=30
        )
        return response.json()
    except requests.exceptions.Timeout:
        return {'error': 'Request timeout - please try again'}
    except requests.exceptions.ConnectionError:
        return {'error': 'Connection error - please check your internet'}
    except Exception as e:
        return {'error': str(e)}

def check_api_health() -> bool:
    """Check if API is healthy"""
    try:
        health_url = API_ENDPOINT.rstrip('/') + '/health'
        response = requests.get(health_url, timeout=10)
        return response.status_code == 200
    except Exception:
        return False

# Initialize session state with persistent loading
if 'history' not in st.session_state:
    st.session_state.history = load_history()
if 'show_api_status' not in st.session_state:
    st.session_state.show_api_status = True
if 'last_load_time' not in st.session_state:
    st.session_state.last_load_time = datetime.now()
if 'last_save_time' not in st.session_state:
    st.session_state.last_save_time = None

# Auto-reload history if file was modified externally (every 30 seconds)
if (datetime.now() - st.session_state.last_load_time).seconds > 30:
    current_history = load_history()
    if len(current_history) != len(st.session_state.history):
        st.session_state.history = current_history
    st.session_state.last_load_time = datetime.now()

def get_sentiment_color(score):
    """Return color based on sentiment score"""
    colors = {1: '#28a745', 0: '#ffc107', -1: '#dc3545'}
    return colors.get(score, '#6c757d')

def get_sentiment_emoji(score):
    """Return emoji based on sentiment score"""
    emojis = {1: '😊', 0: '😐', -1: '😞'}
    return emojis.get(score, '🤔')

# Main app header
st.markdown("""
<div class="main-header">
    <h1>🎯 AI Sentiment Analysis</h1>
    <p>Powered by Meta Llama 3 8B • Real-time Analysis • Smart Caching</p>
</div>
""", unsafe_allow_html=True)

# API Health Check Toast
api_status = check_api_health()
if st.session_state.show_api_status:
    if api_status:
        toast_container = st.container()
        with toast_container:
            col1, col2 = st.columns([10, 1])
            with col1:
                st.success("✅ API is healthy and ready")
            with col2:
                if st.button("✕", key="close_toast"):
                    st.session_state.show_api_status = False
                    st.rerun()
    else:
        st.error("❌ API is currently unavailable")

# Sidebar
with st.sidebar:
    st.header("📊 Analytics")
    
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        
        # Sentiment distribution
        sentiment_counts = df['sentiment_label'].value_counts()
        fig = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title="Sentiment Distribution",
            color_discrete_map={
                'positive': '#28a745',
                'neutral': '#ffc107', 
                'negative': '#dc3545'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Stats
        total = len(df)
        positive = len(df[df['sentiment_score'] == 1])
        neutral = len(df[df['sentiment_score'] == 0])
        negative = len(df[df['sentiment_score'] == -1])
        
        col_stat1, col_stat2 = st.columns(2)
        
        with col_stat1:
            st.metric("Total Analyzed", total)
            st.metric("Positive Rate", f"{(positive/total*100):.1f}%" if total > 0 else "0%")
        
        with col_stat2:
            st.metric("Negative Rate", f"{(negative/total*100):.1f}%" if total > 0 else "0%")
            st.metric("Neutral Rate", f"{(neutral/total*100):.1f}%" if total > 0 else "0%")
        
        # Trend chart
        if len(df) > 1:
            df_sorted = df.sort_values('timestamp')
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=df_sorted['timestamp'],
                y=df_sorted['sentiment_score'],
                mode='lines+markers',
                name='Sentiment Trend',
                line=dict(color='#667eea', width=2)
            ))
            fig_trend.update_layout(
                title="Sentiment Trend Over Time",
                xaxis_title="Time",
                yaxis_title="Sentiment Score",
                height=300,
                showlegend=False
            )
            st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("No analysis history yet")
    
    # Persistence status
    st.markdown("---")
    st.markdown("**💾 Data Status**")
    
    # Check if file exists
    if os.path.exists(DATA_FILE):
        file_size = os.path.getsize(DATA_FILE)
        file_time = datetime.fromtimestamp(os.path.getmtime(DATA_FILE))
        st.markdown(f"• File: {file_size} bytes")
        st.markdown(f"• Modified: {file_time.strftime('%H:%M:%S')}")
        st.markdown(f"• Records: {len(st.session_state.history)}")
    else:
        st.markdown("• No saved data yet")
    
    if 'last_save_time' in st.session_state and st.session_state.last_save_time:
        st.markdown(f"• Last save: {st.session_state.last_save_time.strftime('%H:%M:%S')}")
    else:
        st.markdown("• No saves yet")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("✍️ Analyze Text")
    
    # Text input
    message = st.text_area(
        "Enter text to analyze:",
        placeholder="Type your message, tweet, review, or feedback here...",
        height=150
    )
    
    if st.button("🔍 Analyze Sentiment", type="primary"):
        if message.strip():
            with st.spinner("Analyzing sentiment..."):
                result = analyze_sentiment(message)
            
            if 'error' in result:
                st.error(f"Error: {result['error']}")
            else:
                # Display result
                sentiment = result['sentiment']
                score = sentiment['score']
                label = sentiment['label']
                
                # Add to history and save
                new_entry = {
                    'timestamp': datetime.now(),
                    'message': message,
                    'sentiment_score': score,
                    'sentiment_label': label
                }
                st.session_state.history.append(new_entry)
                save_history()
                st.session_state.last_save_time = datetime.now()
                st.success("💾 Data saved successfully!")
                
                # Show result
                st.success("Analysis Complete!")
                
                col_result1, col_result2, col_result3 = st.columns(3)
                
                with col_result1:
                    st.metric("Sentiment Score", score)
                
                with col_result2:
                    st.metric("Sentiment Label", label.title())
                
                with col_result3:
                    st.markdown(
                        f"<h1 style='text-align: center; color: {get_sentiment_color(score)};'>"
                        f"{get_sentiment_emoji(score)}</h1>",
                        unsafe_allow_html=True
                    )
                
                # Show analyzed text
                st.markdown("**Analyzed Text:**")
                color = get_sentiment_color(score)
                st.markdown(
                    f"<div style='padding: 10px; border-left: 4px solid {color}; "
                    f"background-color: {color}20; border-radius: 5px;'>"
                    f"{message}</div>",
                    unsafe_allow_html=True
                )
        else:
            st.warning("Please enter some text to analyze")

with col2:
    st.header("📈 Recent History")
    
    if st.session_state.history:
        # Show recent 5 analyses
        recent = st.session_state.history[-5:]
        
        for item in reversed(recent):
            with st.container():
                st.markdown(
                    f"<div style='padding: 8px; margin: 5px 0; border-radius: 5px; "
                    f"border-left: 3px solid {get_sentiment_color(item['sentiment_score'])};'>"
                    f"<small>{item['timestamp'].strftime('%H:%M:%S')}</small><br>"
                    f"<strong>{item['sentiment_label'].title()}</strong> "
                    f"{get_sentiment_emoji(item['sentiment_score'])}<br>"
                    f"<em>{item['message'][:50]}{'...' if len(item['message']) > 50 else ''}</em>"
                    f"</div>",
                    unsafe_allow_html=True
                )
        
        # Action buttons
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("🔄 Refresh", help="Reload history from file"):
                st.session_state.history = load_history()
                st.rerun()
        
        with col_btn2:
            if st.button("📥 Export", help="Export to CSV"):
                csv_data = export_to_csv()
                if csv_data:
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name=f"sentiment_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
        
        with col_btn3:
            if st.button("🗑️ Clear", help="Clear all history"):
                st.session_state.confirm_clear = True
                st.rerun()
        
        # Confirmation dialog for clear
        if st.session_state.get('confirm_clear', False):
            st.warning("⚠️ Are you sure you want to clear all history?")
            col_confirm1, col_confirm2 = st.columns(2)
            with col_confirm1:
                if st.button("✅ Yes, Clear All", type="primary"):
                    st.session_state.history = []
                    save_history()
                    st.session_state.confirm_clear = False
                    st.success("History cleared!")
                    st.rerun()
            with col_confirm2:
                if st.button("❌ Cancel"):
                    st.session_state.confirm_clear = False
                    st.rerun()
    else:
        st.info("No recent analyses")

# Footer
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.markdown("**🚀 Features**")
    st.markdown("• Real-time Analysis")
    st.markdown("• Smart Caching")
    st.markdown("• Data Export")

with col_footer2:
    st.markdown("**🔧 Technology**")
    st.markdown("• Meta Llama 3 8B")
    st.markdown("• AWS Bedrock")
    st.markdown("• Streamlit")

with col_footer3:
    st.markdown("**📊 Statistics**")
    total_analyzed = len(st.session_state.history)
    st.markdown(f"• Total Analyzed: {total_analyzed}")
    st.markdown(f"• API Status: {'🟢 Online' if api_status else '🔴 Offline'}")

st.markdown(
    "<div style='text-align: center; color: #666; margin-top: 2rem;'>"
    "Built with ❤️ using Streamlit and AWS Bedrock • "
    f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    "</div>",
    unsafe_allow_html=True
)