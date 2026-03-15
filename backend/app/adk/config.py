"""
ADK Configuration
Manages configuration for Google ADK and Gemini integration
"""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from google.cloud.secretmanager import SecretManagerServiceClient
import structlog


logger = structlog.get_logger()


class ADKConfig(BaseSettings):
    """Configuration for Agent Development Kit"""

    # Google Cloud
    gcp_project: str = Field(default="", alias="GOOGLE_CLOUD_PROJECT")
    gcp_region: str = Field(default="us-central1", alias="GCP_REGION")
    credentials_path: Optional[str] = Field(default=None, alias="GOOGLE_APPLICATION_CREDENTIALS")

    # Gemini Configuration
    gemini_api_key: str = Field(default="")
    gemini_model: str = Field(default="gemini-3-flash-preview")

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
    gemini_api_key_secret_name: str = Field(default="gemini-api-key")

    class Config:
        env_file = ".env"
        case_sensitive = False

    # def get_api_key_from_secret_manager(self, secret_name: str) -> str:
    #     """Get API key from Secret Manager"""
    #     secret_manager = SecretManagerServiceClient()
    #     name = f"projects/{self.gcp_project}/secrets/{secret_name}/versions/latest"
    #     secret_version = secret_manager.access_secret_version(request={"name": name})
    #     return secret_version.payload.data.decode("UTF-8")

def get_config() -> ADKConfig:
    """Get application configuration"""
    # config = ADKConfig()
    # if config.use_secret_manager:
    #     logger.info(f"Getting API key from Secret Manager: {config.gemini_api_key_secret_name}")
    #     config.gemini_api_key = config.get_api_key_from_secret_manager(config.gemini_api_key_secret_name)
    # else:
    #     logger.info("Using API key from environment variables")
    # return config
    return ADKConfig()


get_config()