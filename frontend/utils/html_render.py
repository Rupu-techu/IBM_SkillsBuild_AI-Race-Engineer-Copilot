"""
Helpers for safely rendering HTML fragments in Streamlit.
"""

from __future__ import annotations

from html import escape
from textwrap import dedent

import streamlit as st


def render_html(markup: str) -> None:
    """Render a single self-contained HTML fragment."""
    st.markdown(dedent(markup).strip(), unsafe_allow_html=True)


def escape_html_text(value: object) -> str:
    """Escape dynamic text before embedding it into unsafe HTML."""
    return escape("" if value is None else str(value), quote=True)


def escape_html_multiline(value: object) -> str:
    """Escape dynamic text and preserve newlines for HTML display."""
    return escape_html_text(value).replace("\n", "<br>")
