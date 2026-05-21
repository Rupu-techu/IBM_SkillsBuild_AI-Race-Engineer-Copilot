"""
Sidebar component for race condition inputs
"""

import streamlit as st
from src.core.race_analyzer import RaceConditions, TireCompound, WeatherCondition


def render_sidebar() -> RaceConditions:
    """
    Render sidebar with race condition inputs
    
    Returns:
        RaceConditions object with user inputs
    """
    
    st.sidebar.markdown("## 🎛️ RACE CONTROLS")
    st.sidebar.markdown("---")
    
    # Race Progress Section
    st.sidebar.markdown("### 📊 Race Progress")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        lap_number = st.number_input(
            "Current Lap",
            min_value=1,
            max_value=100,
            value=25,
            step=1,
            help="Current lap number in the race"
        )
    with col2:
        total_laps = st.number_input(
            "Total Laps",
            min_value=1,
            max_value=100,
            value=50,
            step=1,
            help="Total number of laps in the race"
        )
    
    # Position
    position = st.sidebar.number_input(
        "Current Position",
        min_value=1,
        max_value=20,
        value=3,
        step=1,
        help="Current race position"
    )
    
    st.sidebar.markdown("---")
    
    # Tire Section
    st.sidebar.markdown("### 🛞 Tire Status")
    
    tire_compound = st.sidebar.selectbox(
        "Tire Compound",
        options=["soft", "medium", "hard", "intermediate", "wet"],
        index=1,
        help="Current tire compound"
    )
    
    tire_wear = st.sidebar.slider(
        "Tire Wear (%)",
        min_value=0,
        max_value=100,
        value=78,
        step=1,
        help="Current tire degradation percentage"
    )
    
    tire_age = st.sidebar.number_input(
        "Tire Age (laps)",
        min_value=0,
        max_value=50,
        value=16,
        step=1,
        help="Number of laps on current tires"
    )
    
    # Visual tire wear indicator
    if tire_wear < 50:
        tire_status = "🟢 GOOD"
        tire_color = "green"
    elif tire_wear < 80:
        tire_status = "🟡 MODERATE"
        tire_color = "yellow"
    else:
        tire_status = "🔴 CRITICAL"
        tire_color = "red"
    
    st.sidebar.markdown(f"**Status:** <span class='status-{tire_color}'>{tire_status}</span>", 
                       unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Fuel Section
    st.sidebar.markdown("### ⛽ Fuel Management")
    
    fuel_level = st.sidebar.slider(
        "Fuel Level (%)",
        min_value=0,
        max_value=100,
        value=65,
        step=1,
        help="Current fuel level percentage"
    )
    
    # Visual fuel indicator
    if fuel_level < 20:
        fuel_status = "🔴 CRITICAL"
        fuel_color = "red"
    elif fuel_level < 40:
        fuel_status = "🟡 LOW"
        fuel_color = "yellow"
    else:
        fuel_status = "🟢 ADEQUATE"
        fuel_color = "green"
    
    st.sidebar.markdown(f"**Status:** <span class='status-{fuel_color}'>{fuel_status}</span>", 
                       unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Weather Section
    st.sidebar.markdown("### 🌤️ Weather Conditions")
    
    weather = st.sidebar.selectbox(
        "Weather",
        options=["dry", "light_rain", "heavy_rain", "mixed"],
        index=0,
        help="Current weather conditions"
    )
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        track_temp = st.number_input(
            "Track Temp (°C)",
            min_value=0,
            max_value=60,
            value=42,
            step=1,
            help="Track surface temperature"
        )
    with col2:
        air_temp = st.number_input(
            "Air Temp (°C)",
            min_value=0,
            max_value=50,
            value=26,
            step=1,
            help="Ambient air temperature"
        )
    
    st.sidebar.markdown("---")
    
    # Competitive Position Section
    st.sidebar.markdown("### 🏁 Competitive Position")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        gap_to_leader = st.number_input(
            "Gap to Leader (s)",
            min_value=0.0,
            max_value=120.0,
            value=8.5,
            step=0.1,
            help="Time gap to race leader"
        )
    with col2:
        gap_to_behind = st.number_input(
            "Gap Behind (s)",
            min_value=0.0,
            max_value=120.0,
            value=3.2,
            step=0.1,
            help="Time gap to car behind"
        )
    
    st.sidebar.markdown("---")
    
    # Track Conditions Section
    st.sidebar.markdown("### 🚦 Track Status")
    
    track_conditions = st.sidebar.selectbox(
        "Track Conditions",
        options=["green", "yellow", "safety_car"],
        index=0,
        help="Current track status"
    )
    
    # Safety car indicator
    if track_conditions == "safety_car":
        st.sidebar.warning("🚨 SAFETY CAR DEPLOYED")
    elif track_conditions == "yellow":
        st.sidebar.warning("⚠️ YELLOW FLAG")
    else:
        st.sidebar.success("✅ GREEN FLAG")
    
    st.sidebar.markdown("---")
    
    # Driver Mode Section
    st.sidebar.markdown("### 🎮 Driver Mode")
    
    driver_mode = st.sidebar.radio(
        "Aggression Level",
        options=["Conservative", "Balanced", "Aggressive"],
        index=1,
        help="Driver aggression mode"
    )
    
    st.sidebar.markdown("---")
    
    # Analyze Button
    analyze_button = st.sidebar.button(
        "🤖 ANALYZE STRATEGY",
        use_container_width=True,
        type="primary"
    )
    
    if analyze_button:
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
    st.session_state.driver_mode = driver_mode
    
    return race_conditions

# Made with Bob
