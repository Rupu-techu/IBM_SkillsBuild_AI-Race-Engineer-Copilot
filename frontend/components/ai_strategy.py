"""
Hero AI Strategy Component
Main strategy recommendation engine display
"""

from __future__ import annotations

import streamlit as st

from frontend.utils.html_render import escape_html_multiline, escape_html_text, render_html
from src.ai.granite_engine import GraniteEngine
from src.core.race_analyzer import RaceAnalyzer, RaceConditions


def render_hero_ai_strategy(
    race_conditions: RaceConditions,
    race_analyzer: RaceAnalyzer,
    granite_engine: GraniteEngine,
):
    """
    Render hero AI strategy engine panel.

    Args:
        race_conditions: Current race conditions
        race_analyzer: Race analyzer instance
        granite_engine: Granite AI engine instance
    """
    st.markdown("### 🤖 AI STRATEGY ENGINE", unsafe_allow_html=True)

    try:
        recommendation = race_analyzer.analyze_strategy(race_conditions)
        action_text = escape_html_text(recommendation.action.value.replace("_", " ").upper())
        subtitle = escape_html_text(recommendation.expected_outcome)
        confidence_color = (
            "#10B981"
            if recommendation.confidence > 0.75
            else "#FCD34D"
            if recommendation.confidence > 0.5
            else "#FF4D4D"
        )
        confidence_class = (
            "green" if recommendation.confidence > 0.75 else "yellow" if recommendation.confidence > 0.5 else ""
        )

        render_html(
            f"""
            <div class="hero-strategy-card animate-fade-in-up card-accent-red">
                <div class="strategy-action">{action_text}</div>
                <div class="strategy-subtitle">{subtitle}</div>
                <div class="confidence-meter">
                    <div class="confidence-label">CONFIDENCE</div>
                    <div class="confidence-value" style="color: {confidence_color};">
                        {recommendation.confidence * 100:.0f}%
                    </div>
                    <div class="confidence-bar">
                        <div class="progress-container">
                            <div class="progress-fill {confidence_class}"
                                 style="width: {recommendation.confidence * 100:.0f}%;"></div>
                        </div>
                    </div>
                </div>
            </div>
            """
        )

        col1, col2 = st.columns(2)

        with col1:
            risk_colors = {"low": "#10B981", "medium": "#FCD34D", "high": "#FF4D4D"}
            risk_color = risk_colors.get(recommendation.risk_level, "#FCD34D")
            render_html(
                f"""
                <div class="glass-card card-accent-red">
                    <div class="glass-card-header">
                        <span class="glass-card-title">RISK</span>
                    </div>
                    <div style="text-align: center; padding: 0.75rem 0;">
                        <div style="font-family: 'Orbitron', sans-serif; font-size: 1.5rem; font-weight: 800; color: {risk_color};">
                            {escape_html_text(recommendation.risk_level.upper())}
                        </div>
                    </div>
                </div>
                """
            )

        with col2:
            timing_text = (
                escape_html_text(recommendation.timing_window) if recommendation.timing_window else "No specific window"
            )
            timing_color = "#FF7A00" if recommendation.timing_window else "#8B92A0"
            title = "WINDOW" if recommendation.timing_window else "TIMING"
            render_html(
                f"""
                <div class="glass-card card-accent-amber">
                    <div class="glass-card-header">
                        <span class="glass-card-title">{title}</span>
                    </div>
                    <div style="text-align: center; padding: 0.75rem 0;">
                        <div style="font-family: 'Rajdhani', sans-serif; font-size: 1.35rem; font-weight: 700; color: {timing_color}; letter-spacing: 0.05em; text-transform: uppercase;">
                            {timing_text}
                        </div>
                    </div>
                </div>
                """
            )

        try:
            explanation = granite_engine.explain_decision(
                recommendation.to_dict(),
                race_conditions.to_dict(),
            )
        except Exception:
            explanation = recommendation.expected_outcome

        render_html(
            f"""
                <div class="glass-card" style="margin-top: 1rem;">
                    <div class="glass-card-header">
                        <span class="glass-card-title">AI REASONING</span>
                    </div>
                <div style="font-family: 'Inter', sans-serif; font-size: 0.98rem; line-height: 1.75; color: #DDE4EF;">
                    {escape_html_multiline(explanation)}
                </div>
            </div>
            """
        )

        if recommendation.tire_recommendation:
            tire_colors = {
                "soft": "#FF4D4D",
                "medium": "#FCD34D",
                "hard": "#F5F7FA",
                "intermediate": "#10B981",
                "wet": "#2DD4BF",
            }
            tire_value = recommendation.tire_recommendation.value
            tire_color = tire_colors.get(tire_value, "#FCD34D")
            render_html(
                f"""
                <div class="glass-card card-accent-cyan" style="margin-top: 1rem; border-color: {tire_color};">
                    <div class="glass-card-header">
                        <span class="glass-card-title">RECOMMENDED TIRE</span>
                    </div>
                    <div style="text-align: center; padding: 1rem 0;">
                        <div style="font-family: 'Orbitron', sans-serif; font-size: 1.7rem; font-weight: 800; color: {tire_color}; text-transform: uppercase; letter-spacing: 0.06em;">
                            {escape_html_text(tire_value)}
                        </div>
                    </div>
                </div>
                """
            )

        if recommendation.alternative_actions:
            with st.expander("Alternative Strategies", expanded=False):
                for alt in recommendation.alternative_actions:
                    risk = alt.get("risk", "")
                    risk_icon = "🔴" if risk == "high" else "🟡" if risk == "medium" else "🟢"
                    render_html(
                        f"""
                        <div class="glass-card" style="margin-bottom: 0.75rem;">
                            <div style="font-family: 'Rajdhani', sans-serif; font-weight: 700; font-size: 1rem; margin-bottom: 0.5rem; color: #F7F9FC; letter-spacing: 0.03em;">
                                {risk_icon} {escape_html_text(alt.get('action', '').replace('_', ' ').upper())}
                            </div>
                            <div style="font-family: 'Inter', sans-serif; font-size: 0.95rem; color: #DDE4EF; line-height: 1.65;">
                                {escape_html_multiline(alt.get('reason', ''))}
                            </div>
                        </div>
                        """
                    )

        with st.expander("Detailed AI Analysis", expanded=False):
            try:
                scenario_analysis = granite_engine.analyze_race_scenario(race_conditions.to_dict())
                render_html(
                    f"""
                    <div style="font-family: 'Inter', sans-serif; font-size: 0.98rem; line-height: 1.75; color: #DDE4EF;">
                        {escape_html_multiline(scenario_analysis.get('analysis', 'Analysis not available'))}
                    </div>
                    """
                )
            except Exception:
                st.info("Detailed analysis is available once IBM Granite is connected.")

    except Exception as exc:
        st.error(f"Error generating recommendations: {exc}")
        st.info("Running in demo mode. Configure IBM Granite for full AI capabilities.")
