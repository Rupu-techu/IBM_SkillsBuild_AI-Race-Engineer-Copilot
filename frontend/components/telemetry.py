"""
Telemetry panel component for displaying race data
"""

import streamlit as st
from src.core.race_analyzer import RaceConditions


def render_telemetry_panel(race_conditions: RaceConditions):
    """
    Render telemetry panel with current race data
    
    Args:
        race_conditions: Current race conditions
    """
    
    st.markdown("## 📡 LIVE TELEMETRY")
    
    # Race progress bar
    race_progress = (race_conditions.lap_number / race_conditions.total_laps) * 100
    st.progress(race_progress / 100)
    st.markdown(f"**Lap {race_conditions.lap_number} / {race_conditions.total_laps}** ({race_progress:.1f}% complete)")
    
    st.markdown("---")
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🏁 Position",
            value=f"P{race_conditions.position}",
            delta=None
        )
    
    with col2:
        # Tire wear with color coding
        tire_delta = None
        if race_conditions.tire_wear > 80:
            tire_delta = "Critical"
        elif race_conditions.tire_wear > 60:
            tire_delta = "High"
        
        st.metric(
            label="🛞 Tire Wear",
            value=f"{race_conditions.tire_wear:.0f}%",
            delta=tire_delta,
            delta_color="inverse" if tire_delta else "off"
        )
    
    with col3:
        # Fuel level with color coding
        fuel_delta = None
        if race_conditions.fuel_level < 20:
            fuel_delta = "Critical"
        elif race_conditions.fuel_level < 40:
            fuel_delta = "Low"
        
        st.metric(
            label="⛽ Fuel Level",
            value=f"{race_conditions.fuel_level:.0f}%",
            delta=fuel_delta,
            delta_color="inverse" if fuel_delta else "off"
        )
    
    with col4:
        st.metric(
            label="🌡️ Track Temp",
            value=f"{race_conditions.track_temp:.0f}°C",
            delta=None
        )
    
    st.markdown("---")
    
    # Detailed telemetry table
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🛞 Tire Information")
        st.markdown(f"""
        <div class="metric-card">
            <p><strong>Compound:</strong> {race_conditions.tire_compound.value.upper()}</p>
            <p><strong>Age:</strong> {race_conditions.tire_age} laps</p>
            <p><strong>Wear:</strong> {race_conditions.tire_wear:.1f}%</p>
            <p><strong>Status:</strong> <span class="status-{'red' if race_conditions.tire_wear > 80 else 'yellow' if race_conditions.tire_wear > 60 else 'green'}">
                {'CRITICAL' if race_conditions.tire_wear > 80 else 'MODERATE' if race_conditions.tire_wear > 60 else 'GOOD'}
            </span></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🌤️ Weather Data")
        st.markdown(f"""
        <div class="metric-card">
            <p><strong>Conditions:</strong> {race_conditions.weather.value.replace('_', ' ').upper()}</p>
            <p><strong>Track Temp:</strong> {race_conditions.track_temp:.0f}°C</p>
            <p><strong>Air Temp:</strong> {race_conditions.air_temp:.0f}°C</p>
            <p><strong>Track Status:</strong> <span class="status-{'red' if race_conditions.track_conditions == 'safety_car' else 'yellow' if race_conditions.track_conditions == 'yellow' else 'green'}">
                {race_conditions.track_conditions.upper().replace('_', ' ')}
            </span></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Competitive position
    st.markdown("### 🏁 Competitive Position")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <h3 style="color: #06ffa5; margin: 0;">+{race_conditions.gap_to_leader:.1f}s</h3>
            <p style="margin: 5px 0 0 0; color: #888;">Gap to Leader</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <h3 style="color: #ffd60a; margin: 0;">P{race_conditions.position}</h3>
            <p style="margin: 5px 0 0 0; color: #888;">Current Position</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        gap_color = "#e63946" if race_conditions.gap_to_behind < 2.0 else "#06ffa5"
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <h3 style="color: {gap_color}; margin: 0;">+{race_conditions.gap_to_behind:.1f}s</h3>
            <p style="margin: 5px 0 0 0; color: #888;">Gap Behind</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Race situation summary
    st.markdown("### 📊 Race Situation")
    
    # Calculate race phase
    race_progress_pct = (race_conditions.lap_number / race_conditions.total_laps) * 100
    if race_progress_pct < 33:
        race_phase = "EARLY RACE"
        phase_color = "#06ffa5"
    elif race_progress_pct < 66:
        race_phase = "MID RACE"
        phase_color = "#ffd60a"
    else:
        race_phase = "LATE RACE"
        phase_color = "#e63946"
    
    st.markdown(f"""
    <div class="metric-card">
        <p><strong>Race Phase:</strong> <span style="color: {phase_color};">{race_phase}</span></p>
        <p><strong>Laps Remaining:</strong> {race_conditions.total_laps - race_conditions.lap_number}</p>
        <p><strong>Fuel Remaining:</strong> {race_conditions.fuel_level:.0f}%</p>
        <p><strong>Tire Life:</strong> {100 - race_conditions.tire_wear:.0f}%</p>
    </div>
    """, unsafe_allow_html=True)

# Made with Bob
