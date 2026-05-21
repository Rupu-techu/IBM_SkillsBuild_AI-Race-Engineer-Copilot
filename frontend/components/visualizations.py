"""
Plotly visualization components for race data
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from src.core.race_analyzer import RaceConditions
import numpy as np


def render_visualizations(race_conditions: RaceConditions):
    """
    Render Plotly charts for race analysis
    
    Args:
        race_conditions: Current race conditions
    """
    
    st.markdown("## 📊 RACE ANALYTICS")
    st.markdown("---")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs([
        "🛞 Tire Degradation",
        "⛽ Fuel Analysis",
        "📈 Lap Performance",
        "⏱️ Pit Strategy"
    ])
    
    with tab1:
        render_tire_degradation_chart(race_conditions)
    
    with tab2:
        render_fuel_consumption_chart(race_conditions)
    
    with tab3:
        render_lap_performance_chart(race_conditions)
    
    with tab4:
        render_pit_strategy_chart(race_conditions)


def render_tire_degradation_chart(race_conditions: RaceConditions):
    """Render tire degradation visualization"""
    
    st.markdown("### 🛞 Tire Degradation Analysis")
    
    # Simulate tire degradation over laps
    laps = list(range(0, race_conditions.tire_age + 1))
    
    # Calculate degradation curve (exponential)
    base_degradation = 2.5  # Base degradation per lap
    degradation_rate = np.array([
        base_degradation * (1 + (lap * 0.05)) for lap in laps
    ])
    tire_wear_history = np.cumsum(degradation_rate)
    
    # Normalize to current wear
    if len(tire_wear_history) > 0:
        tire_wear_history = (tire_wear_history / tire_wear_history[-1]) * race_conditions.tire_wear
    
    # Project future degradation
    future_laps = list(range(race_conditions.tire_age + 1, min(race_conditions.tire_age + 15, race_conditions.total_laps + 1)))
    future_degradation = []
    current_wear = race_conditions.tire_wear
    
    for i, lap in enumerate(future_laps):
        current_wear += base_degradation * (1 + ((race_conditions.tire_age + i) * 0.05))
        future_degradation.append(min(current_wear, 100))
    
    # Create figure
    fig = go.Figure()
    
    # Historical tire wear
    fig.add_trace(go.Scatter(
        x=laps,
        y=tire_wear_history,
        mode='lines+markers',
        name='Actual Wear',
        line=dict(color='#06ffa5', width=3),
        marker=dict(size=6)
    ))
    
    # Projected tire wear
    if future_degradation:
        fig.add_trace(go.Scatter(
            x=future_laps,
            y=future_degradation,
            mode='lines',
            name='Projected Wear',
            line=dict(color='#ffd60a', width=2, dash='dash')
        ))
    
    # Critical threshold line
    fig.add_hline(
        y=85,
        line_dash="dot",
        line_color="#e63946",
        annotation_text="Critical Threshold",
        annotation_position="right"
    )
    
    # Optimal pit window
    fig.add_hrect(
        y0=75, y1=85,
        fillcolor="#ffd60a",
        opacity=0.2,
        annotation_text="Optimal Pit Window",
        annotation_position="top left"
    )
    
    fig.update_layout(
        title="Tire Degradation Over Time",
        xaxis_title="Lap Number",
        yaxis_title="Tire Wear (%)",
        template="plotly_dark",
        hovermode='x unified',
        height=400,
        paper_bgcolor='rgba(26, 26, 46, 0.8)',
        plot_bgcolor='rgba(26, 26, 46, 0.8)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tire status summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Wear", f"{race_conditions.tire_wear:.1f}%")
    with col2:
        st.metric("Tire Age", f"{race_conditions.tire_age} laps")
    with col3:
        remaining_life = max(0, 100 - race_conditions.tire_wear)
        st.metric("Remaining Life", f"{remaining_life:.1f}%")


def render_fuel_consumption_chart(race_conditions: RaceConditions):
    """Render fuel consumption visualization"""
    
    st.markdown("### ⛽ Fuel Consumption Analysis")
    
    # Calculate fuel consumption rate
    laps_completed = race_conditions.lap_number
    fuel_used = 100 - race_conditions.fuel_level
    fuel_per_lap = fuel_used / laps_completed if laps_completed > 0 else 2.0
    
    # Historical fuel levels
    laps = list(range(0, laps_completed + 1))
    fuel_history = [100 - (fuel_per_lap * lap) for lap in laps]
    
    # Projected fuel levels
    remaining_laps = race_conditions.total_laps - race_conditions.lap_number
    future_laps = list(range(laps_completed + 1, race_conditions.total_laps + 1))
    fuel_projection = [race_conditions.fuel_level - (fuel_per_lap * i) for i in range(1, len(future_laps) + 1)]
    
    # Create figure
    fig = go.Figure()
    
    # Historical fuel
    fig.add_trace(go.Scatter(
        x=laps,
        y=fuel_history,
        mode='lines+markers',
        name='Actual Fuel',
        line=dict(color='#06ffa5', width=3),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(6, 255, 165, 0.2)'
    ))
    
    # Projected fuel
    fig.add_trace(go.Scatter(
        x=future_laps,
        y=fuel_projection,
        mode='lines',
        name='Projected Fuel',
        line=dict(color='#ffd60a', width=2, dash='dash')
    ))
    
    # Critical fuel level
    fig.add_hline(
        y=15,
        line_dash="dot",
        line_color="#e63946",
        annotation_text="Critical Level",
        annotation_position="right"
    )
    
    # Finish line
    fig.add_vline(
        x=race_conditions.total_laps,
        line_dash="dot",
        line_color="white",
        annotation_text="Finish",
        annotation_position="top"
    )
    
    fig.update_layout(
        title="Fuel Level Projection",
        xaxis_title="Lap Number",
        yaxis_title="Fuel Level (%)",
        template="plotly_dark",
        hovermode='x unified',
        height=400,
        paper_bgcolor='rgba(26, 26, 46, 0.8)',
        plot_bgcolor='rgba(26, 26, 46, 0.8)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Fuel metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Fuel", f"{race_conditions.fuel_level:.1f}%")
    with col2:
        st.metric("Consumption Rate", f"{fuel_per_lap:.2f}%/lap")
    with col3:
        fuel_at_finish = race_conditions.fuel_level - (fuel_per_lap * remaining_laps)
        st.metric("Projected at Finish", f"{max(0, fuel_at_finish):.1f}%")


def render_lap_performance_chart(race_conditions: RaceConditions):
    """Render lap performance analysis"""
    
    st.markdown("### 📈 Lap Performance Trends")
    
    # Simulate lap times (for demonstration)
    laps = list(range(1, race_conditions.lap_number + 1))
    
    # Base lap time with tire degradation effect
    base_time = 90.0  # seconds
    lap_times = []
    
    for lap in laps:
        # Calculate tire age at that lap
        if lap <= race_conditions.tire_age:
            tire_age_at_lap = race_conditions.tire_age - (race_conditions.lap_number - lap)
        else:
            tire_age_at_lap = 0
        
        # Degradation effect (slower with older tires)
        degradation_effect = tire_age_at_lap * 0.05
        
        # Add some randomness
        random_variation = np.random.uniform(-0.3, 0.3)
        
        lap_time = base_time + degradation_effect + random_variation
        lap_times.append(lap_time)
    
    # Create figure
    fig = go.Figure()
    
    # Lap times
    fig.add_trace(go.Scatter(
        x=laps,
        y=lap_times,
        mode='lines+markers',
        name='Lap Time',
        line=dict(color='#06ffa5', width=2),
        marker=dict(size=6)
    ))
    
    # Average lap time
    avg_time = np.mean(lap_times)
    fig.add_hline(
        y=avg_time,
        line_dash="dash",
        line_color="#ffd60a",
        annotation_text=f"Average: {avg_time:.2f}s",
        annotation_position="right"
    )
    
    # Best lap time
    best_time = min(lap_times)
    fig.add_hline(
        y=best_time,
        line_dash="dot",
        line_color="#06ffa5",
        annotation_text=f"Best: {best_time:.2f}s",
        annotation_position="right"
    )
    
    fig.update_layout(
        title="Lap Time Evolution",
        xaxis_title="Lap Number",
        yaxis_title="Lap Time (seconds)",
        template="plotly_dark",
        hovermode='x unified',
        height=400,
        paper_bgcolor='rgba(26, 26, 46, 0.8)',
        plot_bgcolor='rgba(26, 26, 46, 0.8)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Best Lap", f"{best_time:.2f}s")
    with col2:
        st.metric("Average Lap", f"{avg_time:.2f}s")
    with col3:
        current_pace = lap_times[-1] if lap_times else base_time
        st.metric("Current Pace", f"{current_pace:.2f}s")


def render_pit_strategy_chart(race_conditions: RaceConditions):
    """Render pit strategy timing visualization"""
    
    st.markdown("### ⏱️ Pit Stop Strategy Windows")
    
    total_laps = race_conditions.total_laps
    current_lap = race_conditions.lap_number
    
    # Define pit windows
    early_window = (int(total_laps * 0.25), int(total_laps * 0.35))
    optimal_window = (int(total_laps * 0.4), int(total_laps * 0.6))
    late_window = (int(total_laps * 0.65), int(total_laps * 0.75))
    
    # Create figure
    fig = go.Figure()
    
    # Race timeline
    fig.add_trace(go.Bar(
        x=[total_laps],
        y=['Race'],
        orientation='h',
        marker=dict(color='rgba(100, 100, 100, 0.3)'),
        name='Race Distance',
        showlegend=False
    ))
    
    # Early pit window
    fig.add_trace(go.Bar(
        x=[early_window[1] - early_window[0]],
        y=['Race'],
        orientation='h',
        marker=dict(color='rgba(255, 214, 10, 0.5)'),
        name='Early Window',
        base=early_window[0]
    ))
    
    # Optimal pit window
    fig.add_trace(go.Bar(
        x=[optimal_window[1] - optimal_window[0]],
        y=['Race'],
        orientation='h',
        marker=dict(color='rgba(6, 255, 165, 0.5)'),
        name='Optimal Window',
        base=optimal_window[0]
    ))
    
    # Late pit window
    fig.add_trace(go.Bar(
        x=[late_window[1] - late_window[0]],
        y=['Race'],
        orientation='h',
        marker=dict(color='rgba(230, 57, 70, 0.5)'),
        name='Late Window',
        base=late_window[0]
    ))
    
    # Current position marker
    fig.add_vline(
        x=current_lap,
        line_color="white",
        line_width=3,
        annotation_text=f"Current: Lap {current_lap}",
        annotation_position="top"
    )
    
    fig.update_layout(
        title="Pit Stop Timing Windows",
        xaxis_title="Lap Number",
        template="plotly_dark",
        height=300,
        paper_bgcolor='rgba(26, 26, 46, 0.8)',
        plot_bgcolor='rgba(26, 26, 46, 0.8)',
        font=dict(color='white'),
        showlegend=True,
        barmode='overlay'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Pit window analysis
    st.markdown("#### Pit Window Analysis")
    
    if early_window[0] <= current_lap <= early_window[1]:
        window_status = "🟡 EARLY WINDOW"
        window_message = "You're in the early pit window. Consider track position and tire condition."
    elif optimal_window[0] <= current_lap <= optimal_window[1]:
        window_status = "🟢 OPTIMAL WINDOW"
        window_message = "You're in the optimal pit window. This is the ideal time for a pit stop."
    elif late_window[0] <= current_lap <= late_window[1]:
        window_status = "🔴 LATE WINDOW"
        window_message = "You're in the late pit window. Pit stop urgency is increasing."
    elif current_lap < early_window[0]:
        window_status = "⏳ TOO EARLY"
        window_message = f"Too early for pit stop. Optimal window opens at lap {optimal_window[0]}."
    else:
        window_status = "⚠️ BEYOND WINDOW"
        window_message = "Beyond typical pit windows. Consider tire condition carefully."
    
    st.info(f"**{window_status}**: {window_message}")
    
    # Pit stop metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Optimal Window", f"Laps {optimal_window[0]}-{optimal_window[1]}")
    with col2:
        laps_to_optimal = max(0, optimal_window[0] - current_lap)
        st.metric("Laps to Optimal", f"{laps_to_optimal}")
    with col3:
        st.metric("Tire Age", f"{race_conditions.tire_age} laps")

# Made with Bob
