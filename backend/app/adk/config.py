"""
ADK Configuration
Manages configuration for Google ADK and Gemini integration
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class ADKConfig(BaseSettings):
    """Configuration for Agent Development Kit"""

    # Google Cloud
    gcp_project: str = Field(default="", alias="GOOGLE_CLOUD_PROJECT")
    gcp_region: str = Field(default="us-central1", alias="GCP_REGION")
    credentials_path: Optional[str] = Field(default=None, alias="GOOGLE_APPLICATION_CREDENTIALS")

    # Gemini Configuration
    gemini_api_key: str = Field(default="")
    gemini_model: str = Field(default="gemini-2.0-flash-exp")

    # Storage
    storage_bucket: Optional[str] = Field(default=None, alias="CLOUD_STORAGE_BUCKET")

    # Application Settings
    port: int = Field(default=8000)
    host: str = Field(default="0.0.0.0")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")

    # CORS
    allowed_origins: str = Field(default="*")

    # Agent Configuration
    max_concurrent_agents: int = Field(default=6)
    stream_timeout: int = Field(default=300)

    # Secret Manager
    use_secret_manager: bool = Field(default=False)

    class Config:
        env_file = ".env"
        case_sensitive = False


def get_config() -> ADKConfig:
    """Get application configuration"""
    return ADKConfig()
