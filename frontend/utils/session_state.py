"""
Session state management for Streamlit app
"""

import streamlit as st


def initialize_session_state():
    """
    Initialize Streamlit session state variables
    """
    
    # Analysis state
    if 'analyze_button_clicked' not in st.session_state:
        st.session_state.analyze_button_clicked = False
    
    # Race conditions
    if 'race_conditions' not in st.session_state:
        st.session_state.race_conditions = None
    
    # Driver mode
    if 'driver_mode' not in st.session_state:
        st.session_state.driver_mode = "Balanced"
    
    # Recommendation history
    if 'recommendation_history' not in st.session_state:
        st.session_state.recommendation_history = []
    
    # Analysis count
    if 'analysis_count' not in st.session_state:
        st.session_state.analysis_count = 0


def reset_session_state():
    """
    Reset session state to initial values
    """
    st.session_state.analyze_button_clicked = False
    st.session_state.race_conditions = None
    st.session_state.recommendation_history = []
    st.session_state.analysis_count = 0


def add_to_history(recommendation: dict):
    """
    Add recommendation to history
    
    Args:
        recommendation: Recommendation dictionary to add
    """
    if 'recommendation_history' not in st.session_state:
        st.session_state.recommendation_history = []
    
    st.session_state.recommendation_history.append(recommendation)
    st.session_state.analysis_count += 1
    
    # Keep only last 10 recommendations
    if len(st.session_state.recommendation_history) > 10:
        st.session_state.recommendation_history = st.session_state.recommendation_history[-10:]

# Made with Bob
