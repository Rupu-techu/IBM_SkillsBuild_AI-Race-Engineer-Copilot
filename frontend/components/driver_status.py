"""
Driver & Race Status Component
F1 driver profile and telemetry display
"""

from __future__ import annotations

import streamlit as st

from frontend.utils.html_render import escape_html_text, render_html
from src.core.race_analyzer import RaceConditions


def render_driver_status(race_conditions: RaceConditions):
    """Render driver profile and race status panel."""
    st.markdown("### 👤 DRIVER STATUS", unsafe_allow_html=True)

    render_html(
        """
        <div class="driver-card animate-fade-in-up card-accent-cyan">
            <div class="driver-avatar">🏎️</div>
            <div class="driver-name">DRIVER</div>
            <div class="driver-team">AI RACE TEAM</div>
        </div>
        """
    )

    render_html(
        f"""
        <div class="glass-card card-accent-red" style="margin-top: 0.75rem;">
            <div class="glass-card-header">
                <span class="glass-card-title">POSITION</span>
            </div>
            <div style="text-align: center; padding: 1rem 0;">
                <div style="font-family: 'Orbitron', sans-serif; font-size: 2.5rem; font-weight: 900; color: #FF4D4D;">
                    P{race_conditions.position}
                </div>
            </div>
        </div>
        """
    )

    gap_behind_color = "#FF4D4D" if race_conditions.gap_to_behind < 2.0 else "#10B981"
    tire_display = race_conditions.tire_compound.value.upper()
    tire_colors = {
        "SOFT": "#FF4D4D",
        "MEDIUM": "#FCD34D",
        "HARD": "#F5F7FA",
        "INTERMEDIATE": "#10B981",
        "WET": "#2DD4BF",
    }
    tire_color = tire_colors.get(tire_display, "#FCD34D")

    render_html(
        f"""
        <div class="glass-card card-accent-cyan" style="margin-top: 0.75rem;">
            <div class="glass-card-header">
                <span class="glass-card-title">LIVE DATA</span>
            </div>
            <div class="telemetry-stat">
                <span class="stat-label">GAP TO LEADER</span>
                <span class="stat-value" style="color: #2DD4BF;">+{race_conditions.gap_to_leader:.1f}s</span>
            </div>
            <div class="telemetry-stat">
                <span class="stat-label">GAP BEHIND</span>
                <span class="stat-value" style="color: {gap_behind_color};">+{race_conditions.gap_to_behind:.1f}s</span>
            </div>
            <div class="telemetry-stat">
                <span class="stat-label">TIRE COMPOUND</span>
                <span class="stat-value" style="color: {tire_color};">{escape_html_text(tire_display)}</span>
            </div>
            <div class="telemetry-stat">
                <span class="stat-label">TIRE AGE</span>
                <span class="stat-value">{race_conditions.tire_age} LAPS</span>
            </div>
        </div>
        """
    )

    tire_health = 100 - race_conditions.tire_wear
    tire_health_color = "#10B981" if tire_health > 40 else "#FCD34D" if tire_health > 20 else "#FF4D4D"
    tire_health_class = "green" if tire_health > 40 else "yellow" if tire_health > 20 else ""
    render_html(
        f"""
        <div class="glass-card card-accent-amber" style="margin-top: 0.75rem;">
            <div class="glass-card-header">
                <span class="glass-card-title">TIRES</span>
            </div>
            <div style="padding: 0.75rem 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-family: 'Rajdhani', sans-serif; font-size: 0.82rem; color: #DDE4EF; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;">HEALTH</span>
                    <span style="font-family: 'Orbitron', sans-serif; font-size: 1.125rem; font-weight: 800; color: {tire_health_color};">
                        {tire_health:.0f}%
                    </span>
                </div>
                <div class="progress-container">
                    <div class="progress-fill {tire_health_class}" style="width: {tire_health:.0f}%;"></div>
                </div>
            </div>
        </div>
        """
    )

    fuel_color = "#10B981" if race_conditions.fuel_level > 40 else "#FCD34D" if race_conditions.fuel_level > 20 else "#FF4D4D"
    fuel_class = "green" if race_conditions.fuel_level > 40 else "yellow" if race_conditions.fuel_level > 20 else ""
    render_html(
        f"""
        <div class="glass-card card-accent-amber" style="margin-top: 0.75rem;">
            <div class="glass-card-header">
                <span class="glass-card-title">FUEL</span>
            </div>
            <div style="padding: 0.75rem 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-family: 'Rajdhani', sans-serif; font-size: 0.82rem; color: #DDE4EF; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;">REMAINING</span>
                    <span style="font-family: 'Orbitron', sans-serif; font-size: 1.125rem; font-weight: 800; color: {fuel_color};">
                        {race_conditions.fuel_level:.0f}%
                    </span>
                </div>
                <div class="progress-container">
                    <div class="progress-fill {fuel_class}" style="width: {race_conditions.fuel_level:.0f}%;"></div>
                </div>
            </div>
        </div>
        """
    )

    weather_display = race_conditions.weather.value.replace("_", " ").title()
    weather_icons = {
        "Dry": "☀️",
        "Light Rain": "🌧️",
        "Heavy Rain": "⛈️",
        "Mixed": "🌦️",
    }
    weather_icon = weather_icons.get(weather_display, "🌤️")
    render_html(
        f"""
        <div class="glass-card card-accent-cyan" style="margin-top: 0.75rem;">
            <div class="glass-card-header">
                <span class="glass-card-title">CONDITIONS</span>
            </div>
            <div style="text-align: center; padding: 0.75rem 0;">
                <div style="font-size: 1.75rem; margin-bottom: 0.375rem;">{weather_icon}</div>
                <div style="font-family: 'Rajdhani', sans-serif; font-size: 1.12rem; font-weight: 700; color: #F7F9FC; text-transform: uppercase; letter-spacing: 0.06em;">
                    {escape_html_text(weather_display)}
                </div>
                <div style="display: flex; justify-content: space-around; margin-top: 0.75rem; gap: 0.75rem;">
                    <div>
                        <div style="font-family: 'Rajdhani', sans-serif; font-size: 0.8rem; color: #DDE4EF; text-transform: uppercase; font-weight: 700; letter-spacing: 0.08em;">TRACK</div>
                        <div style="font-family: 'Orbitron', sans-serif; font-size: 1rem; font-weight: 800; color: #FF7A00;">
                            {race_conditions.track_temp:.0f}°C
                        </div>
                    </div>
                    <div>
                        <div style="font-family: 'Rajdhani', sans-serif; font-size: 0.8rem; color: #DDE4EF; text-transform: uppercase; font-weight: 700; letter-spacing: 0.08em;">AIR</div>
                        <div style="font-family: 'Orbitron', sans-serif; font-size: 1rem; font-weight: 800; color: #2DD4BF;">
                            {race_conditions.air_temp:.0f}°C
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
    )
