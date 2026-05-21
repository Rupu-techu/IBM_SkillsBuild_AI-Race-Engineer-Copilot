"""
Watsonx configuration and diagnostics utilities for the Streamlit frontend.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from dotenv import load_dotenv


LOGGER = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"


def load_environment() -> bool:
    """Load environment variables from the project .env file."""
    loaded = load_dotenv(dotenv_path=ENV_PATH, override=True)
    LOGGER.debug("dotenv load attempted from %s: loaded=%s", ENV_PATH, loaded)
    return loaded


def _clean_env_value(value: Optional[str]) -> str:
    if value is None:
        return ""

    cleaned = value.strip()
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in {"'", '"'}:
        cleaned = cleaned[1:-1].strip()
    return cleaned


def _get_env(*names: str, default: str = "") -> str:
    for name in names:
        value = _clean_env_value(os.getenv(name))
        if value:
            return value
    return default


@dataclass(frozen=True)
class WatsonxConfig:
    api_key: str
    project_id: str
    url: str
    model_id: str
    max_tokens: int
    temperature: float

    @property
    def fingerprint(self) -> str:
        key_tail = self.api_key[-6:] if self.api_key else "missing"
        return "|".join(
            [
                key_tail,
                self.project_id,
                self.url,
                self.model_id,
                str(self.max_tokens),
                str(self.temperature),
            ]
        )


def mask_secret(value: str) -> str:
    """Mask a secret for safe diagnostics."""
    if not value:
        return "(missing)"
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}...{value[-4:]}"


def get_watsonx_config() -> WatsonxConfig:
    """Return sanitized watsonx configuration from environment variables."""
    return WatsonxConfig(
        api_key=_get_env("IBM_WATSONX_APIKEY", "IBM_WATSONX_API_KEY"),
        project_id=_get_env("IBM_WATSONX_PROJECT_ID"),
        url=_get_env("IBM_WATSONX_URL", default="https://us-south.ml.cloud.ibm.com"),
        model_id=_get_env("GRANITE_MODEL_ID", default="ibm/granite-13b-chat-v2"),
        max_tokens=int(_get_env("GRANITE_MAX_TOKENS", default="1024")),
        temperature=float(_get_env("GRANITE_TEMPERATURE", default="0.7")),
    )


def validate_watsonx_config(config: WatsonxConfig) -> Dict[str, str]:
    """Validate the presence of the required watsonx configuration values."""
    errors: Dict[str, str] = {}

    if not config.api_key:
        errors["IBM_WATSONX_APIKEY"] = "Missing API key"
    if not config.project_id:
        errors["IBM_WATSONX_PROJECT_ID"] = "Missing project ID"
    if not config.url:
        errors["IBM_WATSONX_URL"] = "Missing service URL"

    return errors


def build_watsonx_diagnostics(
    config: WatsonxConfig,
    *,
    dotenv_loaded: bool,
    connection_ok: bool,
    mock_mode: bool,
    connection_error: Optional[str],
) -> Dict[str, object]:
    """Create a UI-friendly diagnostics payload."""
    error_text = connection_error or ""
    lowered_error = error_text.lower()

    remediation = ""
    if "no_associated_service_instance_error" in lowered_error:
        remediation = (
            "The watsonx project ID is valid, but that IBM Cloud project is not linked to a "
            "Watson Machine Learning or watsonx.ai runtime instance. Associate the project with "
            "a WML-capable service instance in IBM Cloud, then restart Streamlit."
        )
    elif "api key" in lowered_error or "apikey" in lowered_error or "iam token" in lowered_error:
        remediation = (
            "The credentials reached IBM, but authentication failed. Re-check the API key value, "
            "its IAM permissions, and the target region URL."
        )
    elif "winerror 10013" in lowered_error or "socket" in lowered_error:
        remediation = (
            "Outbound access to IBM Cloud is being blocked locally. Check firewall, antivirus, "
            "proxy, or corporate network restrictions."
        )

    return {
        "env_file_exists": ENV_PATH.exists(),
        "env_path": str(ENV_PATH),
        "dotenv_loaded": dotenv_loaded,
        "api_key_detected": bool(config.api_key),
        "api_key_masked": mask_secret(config.api_key),
        "project_id_detected": bool(config.project_id),
        "project_id_masked": mask_secret(config.project_id),
        "service_url": config.url,
        "active_model": config.model_id,
        "connection_status": "Connected" if connection_ok else "Unavailable",
        "mock_mode": mock_mode,
        "connection_error": error_text,
        "remediation": remediation,
        "config_errors": validate_watsonx_config(config),
    }
