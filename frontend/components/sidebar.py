"""
Racing Sidebar Component
Compact F1 pit wall controls
"""

import streamlit as st
from src.core.race_analyzer import RaceConditions, TireCompound, WeatherCondition


def render_racing_sidebar() -> RaceConditions:
    """
    Render premium racing sidebar with controls
    
    Returns:
        RaceConditions object with user inputs
    """
    
    st.markdown("### ⚙️ RACE CONTROLS", unsafe_allow_html=True)
    
    # Simulation Controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶️", use_container_width=True, help="Start", key="start_btn"):
            st.session_state.simulation_running = True
            st.session_state.current_lap = st.session_state.get('current_lap', 1)
            st.rerun()
    
    with col2:
        if st.button("⏸️", use_container_width=True, help="Pause", key="pause_btn"):
            st.session_state.simulation_running = False
            st.rerun()
    
    with col3:
        if st.button("🔄", use_container_width=True, help="Reset", key="reset_btn"):
            st.session_state.simulation_running = False
            st.session_state.current_lap = 1
            st.session_state.fuel_level = 100.0
            st.session_state.tire_wear = 0.0
            st.rerun()
    
    st.markdown("---", unsafe_allow_html=True)
    
    # Race Progress
    st.markdown("### 📊 RACE", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        lap_number = st.number_input(
            "Lap",
            min_value=1,
            max_value=100,
            value=st.session_state.get('current_lap', 25),
            step=1,
            key="lap_input"
        )
    with col2:
        total_laps = st.number_input(
            "Total",
            min_value=1,
            max_value=100,
            value=58,
            step=1,
            key="total_laps_input"
        )
    
    position = st.number_input(
        "Position",
        min_value=1,
        max_value=20,
        value=3,
        step=1,
        key="position_input"
    )
    
    st.markdown("---", unsafe_allow_html=True)
    
    # Tire Management
    st.markdown("### 🛞 TIRES", unsafe_allow_html=True)
    
    tire_compound = st.selectbox(
        "Compound",
        options=["soft", "medium", "hard", "intermediate", "wet"],
        index=1,
        key="tire_compound_select"
    )
    
    tire_wear = st.slider(
        "Wear %",
        min_value=0,
        max_value=100,
        value=int(st.session_state.get('tire_wear', 78)),
        step=1,
        key="tire_wear_input"
    )
    
    tire_age = st.number_input(
        "Age (laps)",
        min_value=0,
        max_value=50,
        value=st.session_state.get('tire_age', 16),
        step=1,
        key="tire_age_input"
    )
    
    st.markdown("---", unsafe_allow_html=True)
    
    # Fuel
    st.markdown("### ⛽ FUEL", unsafe_allow_html=True)
    
    fuel_level = st.slider(
        "Level %",
        min_value=0,
        max_value=100,
        value=int(st.session_state.get('fuel_level', 65)),
        step=1,
        key="fuel_input"
    )
    
    st.markdown("---", unsafe_allow_html=True)
    
    # Weather
    st.markdown("### 🌤️ WEATHER", unsafe_allow_html=True)
    
    weather = st.selectbox(
        "Conditions",
        options=["dry", "light_rain", "heavy_rain", "mixed"],
        index=0,
        key="weather_select"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        track_temp = st.number_input(
            "Track °C",
            min_value=0,
            max_value=60,
            value=42,
            step=1,
            key="track_temp_input"
        )
    with col2:
        air_temp = st.number_input(
            "Air °C",
            min_value=0,
            max_value=50,
            value=26,
            step=1,
            key="air_temp_input"
        )
    
    st.markdown("---", unsafe_allow_html=True)
    
    # Gaps
    st.markdown("### 🏁 GAPS", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        gap_to_leader = st.number_input(
            "Leader (s)",
            min_value=0.0,
            max_value=120.0,
            value=8.5,
            step=0.1,
            key="gap_leader_input"
        )
    with col2:
        gap_to_behind = st.number_input(
            "Behind (s)",
            min_value=0.0,
            max_value=120.0,
            value=3.2,
            step=0.1,
            key="gap_behind_input"
        )
    
    st.markdown("---", unsafe_allow_html=True)
    
    # Track Status
    st.markdown("### 🚦 TRACK", unsafe_allow_html=True)
    
    track_conditions = st.selectbox(
        "Status",
        options=["green", "yellow", "safety_car"],
        index=0,
        key="track_status_select"
    )
    
    st.markdown("---", unsafe_allow_html=True)
    
    # Analyze Button
    if st.button("🤖 ANALYZE STRATEGY", use_container_width=True, type="primary", key="analyze_btn"):
        st.session_state.analyze_button_clicked = True
    
    # Create RaceConditions object
    race_conditions = RaceConditions(
        lap_number=lap_number,
        total_laps=total_laps,
        tire_wear=float(tire_wear),
        tire_compound=TireCompound(tire_compound),
        tire_age=tire_age,
        weather=WeatherCondition(weather),
        track_temp=float(track_temp),
        air_temp=float(air_temp),
        position=position,
        fuel_level=float(fuel_level),
        gap_to_leader=gap_to_leader,
        gap_to_behind=gap_to_behind,
        track_conditions=track_conditions
    )
    
    # Store in session state
    st.session_state.race_conditions = race_conditions
    
    return race_conditions
