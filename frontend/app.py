"""
AI Race Engineer Copilot - Streamlit Dashboard
Real-time racing strategy assistant with IBM Granite AI
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from frontend.components.sidebar import render_sidebar
from frontend.components.telemetry import render_telemetry_panel
from frontend.components.ai_recommendations import render_ai_recommendations
from frontend.components.visualizations import render_visualizations
from frontend.utils.session_state import initialize_session_state
from src.core.race_analyzer import RaceAnalyzer, RaceConditions, TireCompound, WeatherCondition
from src.ai.granite_engine import GraniteEngine

# Page configuration
st.set_page_config(
    page_title="AI Race Engineer Copilot",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for racing theme
st.markdown("""
<style>
    /* Dark racing theme */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #e63946 0%, #f77f00 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(230, 57, 70, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(26, 26, 46, 0.8);
        border: 2px solid #e63946;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Status indicators */
    .status-green {
        color: #06ffa5;
        font-weight: bold;
    }
    
    .status-yellow {
        color: #ffd60a;
        font-weight: bold;
    }
    
    .status-red {
        color: #e63946;
        font-weight: bold;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #16213e;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #e63946 0%, #f77f00 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(230, 57, 70, 0.5);
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application entry point"""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏎️ AI RACE ENGINEER COPILOT</h1>
        <p style="color: white; margin: 5px 0 0 0; font-size: 14px;">
            Powered by IBM Granite AI | Real-time Strategy Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize engines
    if 'race_analyzer' not in st.session_state:
        st.session_state.race_analyzer = RaceAnalyzer()
    
    if 'granite_engine' not in st.session_state:
        try:
            st.session_state.granite_engine = GraniteEngine()
        except Exception as e:
            st.warning(f"Running in demo mode: {str(e)}")
            st.session_state.granite_engine = GraniteEngine()
    
    # Sidebar inputs
    race_conditions = render_sidebar()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Telemetry panel
        render_telemetry_panel(race_conditions)
        
        # Visualizations
        render_visualizations(race_conditions)
    
    with col2:
        # AI Recommendations
        if st.session_state.get('analyze_button_clicked', False):
            with st.spinner("🤖 AI analyzing race conditions..."):
                render_ai_recommendations(
                    race_conditions,
                    st.session_state.race_analyzer,
                    st.session_state.granite_engine
                )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 12px;">
        <p>AI Race Engineer Copilot | IBM SkillsBuild AI Builders Challenge</p>
        <p>Built with IBM Granite, watsonx.ai, and Langflow</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

# Made with Bob
