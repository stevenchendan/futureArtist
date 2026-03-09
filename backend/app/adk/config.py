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
    gcp_project: str = Field(default="", env="GOOGLE_CLOUD_PROJECT")
    gcp_region: str = Field(default="us-central1", env="GCP_REGION")
    credentials_path: Optional[str] = Field(default=None, env="GOOGLE_APPLICATION_CREDENTIALS")

    # Gemini Configuration
    gemini_api_key: str = Field(default="", env="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-2.0-flash-exp", env="GEMINI_MODEL")

    # Storage
    storage_bucket: Optional[str] = Field(default=None, env="CLOUD_STORAGE_BUCKET")

    # Application Settings
    port: int = Field(default=8000, env="PORT")
    host: str = Field(default="0.0.0.0", env="HOST")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # CORS
    allowed_origins: str = Field(default="*", env="ALLOWED_ORIGINS")

    # Agent Configuration
    max_concurrent_agents: int = Field(default=6, env="MAX_CONCURRENT_AGENTS")
    stream_timeout: int = Field(default=300, env="STREAM_TIMEOUT")

    # Secret Manager
    use_secret_manager: bool = Field(default=False, env="USE_SECRET_MANAGER")

    class Config:
        env_file = ".env"
        case_sensitive = False


def get_config() -> ADKConfig:
    """Get application configuration"""
    return ADKConfig()
