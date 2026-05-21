"""
Track Visualization Component
Animated F1 circuit display with telemetry overlays
"""

from __future__ import annotations

import streamlit as st

from frontend.utils.html_render import escape_html_text, render_html
from src.core.race_analyzer import RaceConditions


TRACK_PATH = (
    "M 128 54 "
    "C 176 34, 242 58, 252 114 "
    "C 260 154, 240 190, 210 204 "
    "C 196 210, 192 224, 200 240 "
    "C 212 264, 192 282, 160 286 "
    "C 108 292, 56 262, 48 214 "
    "C 42 176, 56 148, 82 136 "
    "C 100 128, 108 112, 96 92 "
    "C 88 76, 100 62, 128 54 Z"
)


def _sector_state(current_sector: int, sector_number: int) -> tuple[str, str]:
    if current_sector > sector_number:
        return "CLEARED", "#10B981"
    if current_sector == sector_number:
        return "LIVE", "#FF7A00"
    return "ARMED", "#ADB9CC"


def _track_status(race_conditions: RaceConditions) -> tuple[str, str]:
    if race_conditions.track_conditions == "safety_car":
        return "SAFETY CAR", "#FF4D4D"
    if race_conditions.track_conditions == "yellow":
        return "YELLOW", "#FCD34D"
    return "GREEN", "#10B981"


def render_track_visualization(race_conditions: RaceConditions):
    """Render an animated circuit panel with telemetry overlays."""
    st.markdown("### 🏁 TRACK POSITION", unsafe_allow_html=True)

    race_progress = min(max((race_conditions.lap_number / race_conditions.total_laps) * 100, 0), 100)
    progress_ratio = race_progress / 100
    current_sector = min(3, int(progress_ratio * 3) + 1)
    status_text, status_color = _track_status(race_conditions)
    pace_delta = max(0.2, min(2.8, race_conditions.gap_to_behind))
    car_rotation = 34 + (progress_ratio * 292)
    pulse_color = "#FF4D4D" if race_conditions.track_conditions == "safety_car" else "#2DD4BF"

    render_html(
        f"""
        <div class="track-container animate-fade-in-up card-accent-cyan">
            <div class="track-stage">
                <div class="track-overlay top-left">
                    <div class="track-overlay-label">Race Progress</div>
                    <div class="track-overlay-value">{race_progress:.1f}%</div>
                </div>
                <div class="track-overlay top-right">
                    <div class="track-overlay-label">Track Status</div>
                    <div class="track-overlay-pill" style="color:{status_color}; border-color:{status_color};">
                        {status_text}
                    </div>
                </div>
                <div class="track-overlay bottom-left">
                    <div class="track-overlay-label">Pace Margin</div>
                    <div class="track-overlay-value">+{pace_delta:.1f}s</div>
                </div>
                <div class="track-overlay bottom-right">
                    <div class="track-overlay-label">Current Sector</div>
                    <div class="track-overlay-value">S{current_sector}</div>
                </div>

                <svg viewBox="0 0 300 340" class="track-svg premium-track-svg" xmlns="http://www.w3.org/2000/svg" aria-label="Track telemetry">
                    <defs>
                        <linearGradient id="trackBase" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="rgba(255,255,255,0.14)" />
                            <stop offset="100%" stop-color="rgba(255,255,255,0.05)" />
                        </linearGradient>
                        <linearGradient id="trackGlow" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="#2DD4BF" />
                            <stop offset="50%" stop-color="#7EE7D9" />
                            <stop offset="100%" stop-color="#FF7A00" />
                        </linearGradient>
                        <filter id="trackSoftGlow" x="-50%" y="-50%" width="200%" height="200%">
                            <feGaussianBlur stdDeviation="6" result="blur" />
                            <feMerge>
                                <feMergeNode in="blur" />
                                <feMergeNode in="SourceGraphic" />
                            </feMerge>
                        </filter>
                        <filter id="carGlow" x="-50%" y="-50%" width="200%" height="200%">
                            <feGaussianBlur stdDeviation="3.5" result="blur" />
                            <feMerge>
                                <feMergeNode in="blur" />
                                <feMergeNode in="SourceGraphic" />
                            </feMerge>
                        </filter>
                    </defs>

                    <g transform="translate(0 10)">
                        <path d="{TRACK_PATH}" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="{TRACK_PATH}" fill="none" stroke="url(#trackBase)" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="{TRACK_PATH}" class="track-energy-line" fill="none" stroke="url(#trackGlow)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" filter="url(#trackSoftGlow)" pathLength="100" stroke-dasharray="34 100" stroke-dashoffset="{100 - race_progress:.1f}"/>

                        <line x1="118" y1="49" x2="142" y2="61" stroke="#FF4D4D" stroke-width="4" stroke-linecap="round"/>
                        <line x1="142" y1="61" x2="156" y2="42" stroke="#F7F9FC" stroke-width="4" stroke-linecap="round"/>

                        <circle cx="88" cy="132" r="4.5" fill="#FCD34D"/>
                        <circle cx="214" cy="127" r="4.5" fill="#FCD34D"/>
                        <circle cx="116" cy="253" r="4.5" fill="#FCD34D"/>

                        <g transform="translate(150 170) rotate({car_rotation}) translate(0 -112)">
                            <circle cx="0" cy="0" r="18" fill="none" stroke="{pulse_color}" stroke-width="2" opacity="0.45">
                                <animate attributeName="r" values="15;22;15" dur="1.8s" repeatCount="indefinite" />
                                <animate attributeName="opacity" values="0.55;0.10;0.55" dur="1.8s" repeatCount="indefinite" />
                            </circle>
                            <circle cx="0" cy="0" r="8.5" fill="{pulse_color}" filter="url(#carGlow)" />
                            <rect x="-6.5" y="-11" width="13" height="22" rx="5" fill="#F7F9FC" opacity="0.96" />
                            <rect x="-3.2" y="-8.5" width="6.4" height="17" rx="2.8" fill="#0A0E17" opacity="0.88" />
                        </g>
                    </g>
                </svg>
            </div>

            <div class="track-telemetry-band">
                <div class="track-telemetry-chip">
                    <span class="track-chip-label">Lap</span>
                    <span class="track-chip-value">{race_conditions.lap_number:02d}</span>
                </div>
                <div class="track-telemetry-chip">
                    <span class="track-chip-label">Window</span>
                    <span class="track-chip-value">{race_conditions.total_laps - race_conditions.lap_number:02d} left</span>
                </div>
                <div class="track-telemetry-chip">
                    <span class="track-chip-label">Track Temp</span>
                    <span class="track-chip-value">{race_conditions.track_temp:.0f}°C</span>
                </div>
            </div>
        </div>
        """
    )

    sectors_markup = []
    for sector_number in range(1, 4):
        sector_state, sector_color = _sector_state(current_sector, sector_number)
        sectors_markup.append(
            f"""
            <div class="telemetry-stat">
                <span class="stat-label">SECTOR {sector_number}</span>
                <span class="stat-value" style="color: {sector_color};">{escape_html_text(sector_state)}</span>
            </div>
            """
        )

    render_html(
        f"""
        <div class="glass-card card-accent-amber" style="margin-top: 0.75rem;">
            <div class="glass-card-header">
                <span class="glass-card-title">SECTOR TIMING</span>
            </div>
            <div class="card-stack-tight">
                {''.join(sectors_markup)}
            </div>
        </div>
        """
    )

    render_html(
        f"""
        <div class="glass-card card-accent-cyan" style="margin-top: 0.75rem;">
            <div class="glass-card-header">
                <span class="glass-card-title">TRACK CONTROL</span>
            </div>
            <div class="card-stack-tight">
                <div class="telemetry-stat">
                    <span class="stat-label">Status</span>
                    <span class="stat-value" style="color: {status_color};">{escape_html_text(status_text)}</span>
                </div>
                <div class="telemetry-stat">
                    <span class="stat-label">Air Temp</span>
                    <span class="stat-value">{race_conditions.air_temp:.0f}°C</span>
                </div>
                <div class="telemetry-stat">
                    <span class="stat-label">Weather</span>
                    <span class="stat-value">{escape_html_text(race_conditions.weather.value.replace('_', ' ').upper())}</span>
                </div>
            </div>
        </div>
        """
    )
