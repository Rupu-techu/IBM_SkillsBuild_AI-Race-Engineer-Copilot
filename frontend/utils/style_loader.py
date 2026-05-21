"""
Centralized stylesheet loading for the Streamlit frontend.
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PRIMARY_STYLESHEET = PROJECT_ROOT / "frontend" / "styles" / "app.css"


def inject_primary_stylesheet() -> None:
    """Inject the single active frontend stylesheet into Streamlit."""
    if not PRIMARY_STYLESHEET.exists():
        raise FileNotFoundError(f"Primary stylesheet not found: {PRIMARY_STYLESHEET}")

    stylesheet = PRIMARY_STYLESHEET.read_text(encoding="utf-8")
    version = int(PRIMARY_STYLESHEET.stat().st_mtime)
    st.markdown(
        f"<style id='frontend-theme' data-version='{version}'>{stylesheet}</style>",
        unsafe_allow_html=True,
    )
