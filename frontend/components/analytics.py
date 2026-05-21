"""
Analytics Section Component
Lower dashboard analytics cards with charts
"""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from frontend.utils.html_render import escape_html_text, render_html
from src.core.race_analyzer import RaceConditions


def _render_chart_card_header(title: str) -> None:
    render_html(
        f"""
        <div class="analytics-card-marker"></div>
        <div class="glass-card-header analytics-card-header">
            <span class="glass-card-title">{escape_html_text(title)}</span>
        </div>
        """
    )


def _render_chart_status(status: str, color: str) -> None:
    render_html(
        f"""
        <div style="text-align: center; padding: 0.75rem; background: rgba(0,0,0,0.3); border-radius: 0.5rem; border: 1px solid {color}; margin-top: 0.5rem;">
            <span style="font-family: 'Rajdhani', sans-serif; font-weight: 700; font-size: 0.875rem; color: {color}; text-transform: uppercase; letter-spacing: 0.05em;">
                {escape_html_text(status)}
            </span>
        </div>
        """
    )


def render_analytics_section(race_conditions: RaceConditions):
    """Render lower analytics cards section."""
    st.markdown("### 📈 RACE ANALYTICS", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        render_tire_degradation_card(race_conditions)

    with col2:
        render_fuel_strategy_card(race_conditions)

    with col3:
        render_pit_window_card(race_conditions)


def render_tire_degradation_card(race_conditions: RaceConditions):
    """Render tire degradation analytics card."""
    _render_chart_card_header("TIRE DEGRADATION")

    laps = list(range(0, race_conditions.tire_age + 1))
    base_degradation = 2.5
    degradation_rate = np.array([base_degradation * (1 + (lap * 0.05)) for lap in laps])
    tire_wear_history = np.cumsum(degradation_rate)

    if len(tire_wear_history) > 0:
        tire_wear_history = (tire_wear_history / tire_wear_history[-1]) * race_conditions.tire_wear

    future_laps = list(
        range(
            race_conditions.tire_age + 1,
            min(race_conditions.tire_age + 8, race_conditions.total_laps + 1),
        )
    )
    future_degradation = []
    current_wear = race_conditions.tire_wear

    for i, _lap in enumerate(future_laps):
        current_wear += base_degradation * (1 + ((race_conditions.tire_age + i) * 0.05))
        future_degradation.append(min(current_wear, 100))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=laps,
            y=tire_wear_history,
            mode="lines",
            name="Actual",
            line=dict(color="#10B981", width=3),
            fill="tozeroy",
            fillcolor="rgba(16, 185, 129, 0.2)",
        )
    )

    if future_degradation:
        fig.add_trace(
            go.Scatter(
                x=future_laps,
                y=future_degradation,
                mode="lines",
                name="Projected",
                line=dict(color="#FCD34D", width=2, dash="dash"),
            )
        )

    fig.add_hline(y=85, line_dash="dot", line_color="#FF4D4D", annotation_text="Critical", annotation_position="right")
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=10, color="#B8C0CC"),
        margin=dict(l=35, r=15, t=5, b=35),
        height=200,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=9, color="#F5F7FA")),
        xaxis=dict(title="Lap", gridcolor="rgba(255, 255, 255, 0.08)", title_font=dict(size=10, color="#B8C0CC")),
        yaxis=dict(title="Wear %", gridcolor="rgba(255, 255, 255, 0.08)", title_font=dict(size=10, color="#B8C0CC")),
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_fuel_strategy_card(race_conditions: RaceConditions):
    """Render fuel strategy analytics card."""
    _render_chart_card_header("FUEL STRATEGY")

    laps_completed = race_conditions.lap_number
    fuel_used = 100 - race_conditions.fuel_level
    fuel_per_lap = fuel_used / laps_completed if laps_completed > 0 else 2.0

    laps = list(range(0, laps_completed + 1))
    fuel_history = [100 - (fuel_per_lap * lap) for lap in laps]
    future_laps = list(range(laps_completed + 1, race_conditions.total_laps + 1))
    fuel_projection = [
        race_conditions.fuel_level - (fuel_per_lap * i) for i in range(1, len(future_laps) + 1)
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=laps,
            y=fuel_history,
            mode="lines",
            name="Actual",
            line=dict(color="#10B981", width=3),
            fill="tozeroy",
            fillcolor="rgba(16, 185, 129, 0.2)",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=future_laps,
            y=fuel_projection,
            mode="lines",
            name="Projected",
            line=dict(color="#FCD34D", width=2, dash="dash"),
        )
    )
    fig.add_hline(y=15, line_dash="dot", line_color="#FF4D4D", annotation_text="Critical", annotation_position="right")
    fig.add_vline(
        x=race_conditions.total_laps,
        line_dash="dot",
        line_color="#C9D1D9",
        annotation_text="Finish",
        annotation_position="top",
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=10, color="#B8C0CC"),
        margin=dict(l=35, r=15, t=5, b=35),
        height=220,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=9)),
        xaxis=dict(title="Lap", gridcolor="rgba(245, 247, 250, 0.1)", title_font=dict(size=10)),
        yaxis=dict(title="Fuel %", gridcolor="rgba(245, 247, 250, 0.1)", title_font=dict(size=10)),
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_pit_window_card(race_conditions: RaceConditions):
    """Render pit window timeline card."""
    _render_chart_card_header("PIT WINDOWS")

    total_laps = race_conditions.total_laps
    current_lap = race_conditions.lap_number
    early_window = (int(total_laps * 0.25), int(total_laps * 0.35))
    optimal_window = (int(total_laps * 0.4), int(total_laps * 0.6))
    late_window = (int(total_laps * 0.65), int(total_laps * 0.75))

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=[total_laps],
            y=["Pit Windows"],
            orientation="h",
            marker=dict(color="rgba(42, 47, 58, 0.3)"),
            name="Race",
            showlegend=False,
        )
    )

    windows = [
        (early_window, "Early", "#FF7A00"),
        (optimal_window, "Optimal", "#10B981"),
        (late_window, "Late", "#FF4D4D"),
    ]
    for (start, end), name, color in windows:
        fig.add_trace(
            go.Bar(
                x=[end - start],
                y=["Pit Windows"],
                orientation="h",
                marker=dict(color=color, opacity=0.7),
                name=name,
                base=start,
            )
        )

    fig.add_vline(
        x=current_lap,
        line_color="#F5F7FA",
        line_width=3,
        annotation_text=f"Lap {current_lap}",
        annotation_position="top",
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=10, color="#C9D1D9"),
        margin=dict(l=100, r=20, t=10, b=40),
        height=180,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=9)),
        xaxis=dict(title="Lap", gridcolor="rgba(245, 247, 250, 0.1)", title_font=dict(size=10)),
        yaxis=dict(showticklabels=False),
        barmode="overlay",
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    if early_window[0] <= current_lap <= early_window[1]:
        status = "EARLY WINDOW"
        color = "#FF7A00"
    elif optimal_window[0] <= current_lap <= optimal_window[1]:
        status = "OPTIMAL WINDOW"
        color = "#10B981"
    elif late_window[0] <= current_lap <= late_window[1]:
        status = "LATE WINDOW"
        color = "#FF4D4D"
    elif current_lap < early_window[0]:
        status = "TOO EARLY"
        color = "#2DD4BF"
    else:
        status = "BEYOND WINDOW"
        color = "#FCD34D"

    _render_chart_status(status, color)
