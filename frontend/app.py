"""
AI Race Engineer Copilot - Streamlit dashboard entrypoint.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from frontend.utils.watsonx_config import (  # noqa: E402
    build_watsonx_diagnostics,
    get_watsonx_config,
    load_environment,
)
from frontend.utils.style_loader import inject_primary_stylesheet  # noqa: E402
from frontend.utils.html_render import render_html  # noqa: E402


load_environment()
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
LOGGER = logging.getLogger(__name__)

from frontend.components.ai_strategy import render_hero_ai_strategy  # noqa: E402
from frontend.components.analytics import render_analytics_section  # noqa: E402
from frontend.components.driver_status import render_driver_status  # noqa: E402
from frontend.components.sidebar import render_racing_sidebar  # noqa: E402
from frontend.components.track_viz import render_track_visualization  # noqa: E402
from frontend.utils.session_state import initialize_session_state  # noqa: E402
from frontend.utils.simulation import update_simulation  # noqa: E402
from src.ai.granite_engine import GraniteEngine  # noqa: E402
from src.core.race_analyzer import RaceAnalyzer  # noqa: E402


st.set_page_config(
    page_title="AI Race Engineer Copilot",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _classify_error(message: str) -> str:
    lowered = message.lower()
    if "missing" in lowered:
        return "Missing environment variables"
    if "no_associated_service_instance_error" in lowered:
        return "IBM project association issue"
    if "apikey" in lowered or "api key" in lowered or "iam token" in lowered:
        return "Authentication issue"
    if "project" in lowered:
        return "Project configuration issue"
    if (
        "dns" in lowered
        or "host" in lowered
        or "connection" in lowered
        or "timeout" in lowered
        or "forbidden" in lowered
        or "winerror 10013" in lowered
        or "socket" in lowered
    ):
        return "Network connectivity issue"
    return "Initialization error"


def initialize_granite_engine():
    """Create or refresh the Granite engine when config changes."""
    config = get_watsonx_config()
    fingerprint = config.fingerprint

    if "race_analyzer" not in st.session_state:
        st.session_state.race_analyzer = RaceAnalyzer()

    should_recreate = (
        "granite_engine" not in st.session_state
        or st.session_state.get("watsonx_config_fingerprint") != fingerprint
    )

    if should_recreate:
        st.session_state.watsonx_config_fingerprint = fingerprint
        st.session_state.granite_engine = GraniteEngine()

    engine = st.session_state.granite_engine
    diagnostics = build_watsonx_diagnostics(
        config,
        dotenv_loaded=load_environment(),
        connection_ok=engine.connection_ok,
        mock_mode=engine.mock_mode,
        connection_error=engine.initialization_error,
    )

    LOGGER.info("API KEY EXISTS: %s", diagnostics["api_key_detected"])
    LOGGER.info("PROJECT ID EXISTS: %s", diagnostics["project_id_detected"])
    LOGGER.info("URL: %s", diagnostics["service_url"])
    LOGGER.info("MODEL: %s", diagnostics["active_model"])

    print("API KEY EXISTS:", diagnostics["api_key_detected"])
    print("PROJECT ID EXISTS:", diagnostics["project_id_detected"])
    print("URL:", diagnostics["service_url"])
    print("API KEY MASKED:", diagnostics["api_key_masked"])
    print("PROJECT ID MASKED:", diagnostics["project_id_masked"])

    st.session_state.watsonx_diagnostics = diagnostics
    return engine, diagnostics


def render_startup_validation_panel(diagnostics: dict):
    """Render the developer diagnostics panel."""
    with st.expander("Watsonx Diagnostics", expanded=diagnostics["mock_mode"]):
        metric_cols = st.columns(3)
        metric_cols[0].metric("dotenv loaded", "Yes" if diagnostics["dotenv_loaded"] else "No")
        metric_cols[1].metric("API key detected", "Yes" if diagnostics["api_key_detected"] else "No")
        metric_cols[2].metric(
            "Project ID detected", "Yes" if diagnostics["project_id_detected"] else "No"
        )

        metric_cols = st.columns(3)
        metric_cols[0].metric("Connection", diagnostics["connection_status"])
        metric_cols[1].metric("Mock mode", "Enabled" if diagnostics["mock_mode"] else "Disabled")
        metric_cols[2].metric("Env file", "Present" if diagnostics["env_file_exists"] else "Missing")

        st.caption(f"Env path: `{diagnostics['env_path']}`")
        st.caption(f"Model: `{diagnostics['active_model']}`")
        st.caption(f"Service URL: `{diagnostics['service_url']}`")
        st.caption(f"API key: `{diagnostics['api_key_masked']}`")
        st.caption(f"Project ID: `{diagnostics['project_id_masked']}`")

        if diagnostics["config_errors"]:
            st.error(
                "Configuration issues detected: "
                + ", ".join(
                    f"{name} ({message})" for name, message in diagnostics["config_errors"].items()
                )
            )

        if diagnostics["connection_error"]:
            st.error(
                f"{_classify_error(diagnostics['connection_error'])}: {diagnostics['connection_error']}"
            )
        if diagnostics.get("remediation"):
            st.info(diagnostics["remediation"])


inject_primary_stylesheet()
initialize_session_state()
granite_engine, diagnostics = initialize_granite_engine()

if st.session_state.get("simulation_running", False):
    update_simulation()

st.markdown(
    """
    <div class="top-nav animate-fade-in-up">
        <div class="nav-brand">
            <div class="nav-title">AI RACE ENGINEER COPILOT</div>
            <div class="nav-badge">IBM GRANITE</div>
        </div>
        <div class="nav-status">
            <span class="status-dot"></span>
            <span style="font-size: 0.875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                LIVE SESSION
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

render_html(
    """
    <div class="dashboard-intro">
        <div class="dashboard-kicker">Formula 1 Strategy Console</div>
        <div class="dashboard-headline">Race control signals, AI strategy, and telemetry aligned on one pit wall.</div>
    </div>
    """
)

if diagnostics["mock_mode"]:
    st.warning(
        "watsonx.ai is not connected. The app is using mock responses until the startup issue is resolved."
    )
else:
    st.success(f"watsonx.ai connected successfully with model `{diagnostics['active_model']}`.")

render_startup_validation_panel(diagnostics)

with st.sidebar:
    race_conditions = render_racing_sidebar()

render_html('<div class="main-grid-marker"></div>')
main_dashboard = st.container()

with main_dashboard:
    col_left, col_center, col_right = st.columns([0.95, 1.35, 1.0], gap="medium")

    with col_left:
        render_track_visualization(race_conditions)

    with col_center:
        render_hero_ai_strategy(
            race_conditions,
            st.session_state.race_analyzer,
            granite_engine,
        )

    with col_right:
        render_driver_status(race_conditions)

render_html(
    """
    <div class="section-divider">
        <div class="section-divider-line"></div>
        <div class="section-divider-label">Analytics Deck</div>
    </div>
    <div class="analytics-grid-marker"></div>
    """
)
analytics_dashboard = st.container()
with analytics_dashboard:
    render_analytics_section(race_conditions)
