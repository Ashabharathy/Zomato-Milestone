import streamlit as st
import requests
import json
import os
from datetime import datetime
import plotly.express as px
import pandas as pd

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_TOKEN = os.getenv("API_TOKEN", "")

# Page configuration
st.set_page_config(
    page_title="Restaurant Recommendation System",
    page_icon="🍽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B35 0%, #FF8A65 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .restaurant-card {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: #F8F9FA;
        border-left: 4px solid #FF6B35;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    .success-metric {
        color: #2E7D32;
        font-weight: bold;
    }
    .warning-metric {
        color: #FF9800;
        font-weight: bold;
    }
    .error-metric {
        color: #F44336;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# API Client
class APIClient:
    def __init__(self, base_url=API_BASE_URL, token=API_TOKEN):
        self.base_url = base_url
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}" if token else "",
            "Content-Type": "application/json"
        }
    
    def get(self, endpoint):
        try:
            response = requests.get(f"{self.base_url}{endpoint}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")
            return None
    
    def post(self, endpoint, data):
        try:
            response = requests.post(f"{self.base_url}{endpoint}", 
                                   json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")
            return None

# Initialize API client
api = APIClient()

# Sidebar Navigation
with st.sidebar:
    st.title("🍽 Navigation")
    
    page = st.selectbox("Select Page", [
        "Dashboard",
        "Recommendations", 
        "Analytics",
        "Settings"
    ])
    
    # User authentication section
    if not API_TOKEN:
        st.warning("⚠️ API Token Required")
        API_TOKEN = st.text_input("Enter API Token", type="password")
        if API_TOKEN:
            st.success("Token configured!")
            st.rerun()

# Main Content
if page == "Dashboard":
    st.markdown('<div class="main-header"><h2>📊 Dashboard</h2></div>', unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card"><h3>Total Restaurants</h3><h2 class="success-metric">1,234</h2></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card"><h3>Active Users</h3><h2 class="success-metric">456</h2></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card"><h3>Recommendations</h3><h2 class="success-metric">2,789</h2></div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card"><h3>Success Rate</h3><h2 class="warning-metric">87.3%</h2></div>', unsafe_allow_html=True)
    
    # Recent Activity Chart
    st.subheader("📈 Recent Activity")
    
    # Sample data for demonstration
    dates = pd.date_range(start="2024-01-01", end="2024-01-07", freq="D")
    recommendations = [120, 145, 167, 189, 156, 178, 201, 223, 245, 267, 289]
    
    fig = px.line(x=dates, y=recommendations, 
                   title="Daily Recommendations",
                   labels={'x': 'Date', 'y': 'Recommendations'})
    fig.update_layout(showlegend=False, height=300)
    st.plotly_chart(fig, use_container_width=True)

elif page == "Recommendations":
    st.markdown('<div class="main-header"><h2>🍽 Restaurant Recommendations</h2></div>', unsafe_allow_html=True)
    
    # Search and Filter
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search Restaurants", placeholder="Enter restaurant name or cuisine...")
        
    with col2:
        cuisine_filter = st.selectbox("🍴 Cuisine", 
                                ["All", "Italian", "Chinese", "Indian", "Mexican", "American"])
    
    # Get recommendations
    if st.button("🔍 Get Recommendations"):
        with st.spinner("Getting recommendations..."):
            recommendations = api.get("/api/v1/recommendations")
            
            if recommendations:
                for i, restaurant in enumerate(recommendations[:5]):
                    st.markdown(f'''
                    <div class="restaurant-card">
                        <h3>{restaurant.get("name", "Restaurant Name")}</h3>
                        <p><strong>Cuisine:</strong> {restaurant.get("cuisine", "Unknown")}</p>
                        <p><strong>Rating:</strong> ⭐ {restaurant.get("rating", "N/A")}</p>
                        <p><strong>Price Range:</strong> {restaurant.get("price_range", "$$")}</p>
                        <p><strong>Distance:</strong> {restaurant.get("distance", "N/A")} km</p>
                        <p><strong>Why Recommended:</strong> {restaurant.get("explanation", "Based on your preferences")}</p>
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.error("❌ No recommendations available")

elif page == "Analytics":
    st.markdown('<div class="main-header"><h2>📊 Analytics & Insights</h2></div>', unsafe_allow_html=True)
    
    # Analytics tabs
    tab1, tab2, tab3 = st.tabs(["📈 Performance", "👥 User Behavior", "🎯 Business Insights"])
    
    with tab1:
        st.subheader("System Performance")
        
        # Performance metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("API Response Time", "245ms", "↓ 12%", delta=-33)
            st.metric("Database Query Time", "89ms", "↓ 5%", delta=-5)
            
        with col2:
            st.metric("Cache Hit Rate", "92.3%", "↑ 3.4%", delta=3.1)
            st.metric("Success Rate", "98.7%", "↑ 1.2%", delta=1.2)
    
    with tab2:
        st.subheader("User Behavior Analytics")
        
        # Sample user behavior data
        user_data = {
            'Page': ['Dashboard', 'Search', 'Recommendations', 'Profile'],
            'Views': [2341, 1876, 3456, 1234],
            'Avg Time (min)': [5.2, 3.8, 8.1, 4.2]
        }
        
        df_user = pd.DataFrame(user_data)
        st.bar_chart(df_user, x='Page', y='Views', title="Page Views")
        
        # Time spent chart
        fig_time = px.bar(df_user, x='Page', y='Avg Time (min)', 
                          title="Average Time Spent", color='orange')
        st.plotly_chart(fig_time, use_container_width=True)
    
    with tab3:
        st.subheader("Business Intelligence")
        
        # Sample business metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Revenue", "$45,678", "↑ 8.3%", delta=3456)
            st.metric("Active Restaurants", "1,234", "↑ 2.1%", delta=25)
            
        with col2:
            st.metric("Avg Order Value", "$23.45", "↑ 4.7%", delta=1.05)
            st.metric("Customer Satisfaction", "4.6/5.0", "↑ 3.2%", delta=0.15)

elif page == "Settings":
    st.markdown('<div class="main-header"><h2>⚙️ Settings</h2></div>', unsafe_allow_html=True)
    
    # Configuration settings
    st.subheader("🔧 System Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("API Base URL", value=API_BASE_URL, key="api_url")
        st.text_input("Database Host", value="localhost", key="db_host")
        st.number_input("Database Port", value=5432, key="db_port")
        
    with col2:
        st.selectbox("Environment", ["Development", "Staging", "Production"], key="env")
        st.checkbox("Enable Debug Mode", value=False, key="debug")
        st.checkbox("Enable Monitoring", value=True, key="monitoring")
    
    # User preferences
    st.subheader("👤 User Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Location", value="New York, NY", key="location")
        st.selectbox("Preferred Cuisine", 
                   ["All", "Italian", "Chinese", "Indian", "Mexican", "American"], 
                   key="pref_cuisine")
        
    with col2:
        st.slider("Price Range ($)", 10, 200, 50, key="price_range")
        st.slider("Max Distance (km)", 1, 20, 5, key="max_distance")
        st.checkbox("Vegetarian Options Only", value=False, key="vegetarian")
    
    if st.button("💾 Save Settings"):
        st.success("✅ Settings saved successfully!")
        st.balloons()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 2rem;'>
    <p>🍽 Restaurant Recommendation System - Phase 7 Deployment</p>
    <p>Built with ❤️ using Streamlit | FastAPI Backend</p>
</div>
""", unsafe_allow_html=True)
