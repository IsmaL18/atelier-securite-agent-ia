"""
Configuration management for the conference agent.

This module handles all configuration using Pydantic Settings,
loading values from environment variables and .env files.
"""

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Déterminer le chemin de la racine du projet
_PROJECT_ROOT = Path(__file__).parent.parent.parent
_ENV_FILE = _PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings can be overridden via environment variables or .env file.
    """
    
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # LLM Configuration
    llm_provider: Literal["vertex_ai", "gemini", "ollama"] = Field(
        default="vertex_ai",
        description="LLM provider to use"
    )
    llm_model: str = Field(
        default="gemini-2.0-flash-exp",
        description="Model name/ID to use"
    )
    llm_temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Temperature for LLM responses"
    )
    llm_max_tokens: int = Field(
        default=2048,
        ge=1,
        description="Maximum tokens for LLM responses"
    )

    # Ollama Configuration
    ollama_base_url: str | None = Field(
        default="http://127.0.0.1:11434/v1",
        description="Ollama API base URL"
    )
    
    # Google Cloud / Vertex AI
    google_application_credentials: str | None = Field(
        default=None,
        description="Path to Google Cloud service account JSON"
    )
    gemini_api_key: str | None = Field(
        default=None,
        description="Google AI Studio API key (alternative to Vertex AI service account)"
    )
    gcp_project_id: str | None = Field(
        default=None,
        description="GCP project ID"
    )
    gcp_region: str = Field(
        default="us-central1",
        description="GCP region"
    )
    
    # Application Settings
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level"
    )

    # SMTP Email Configuration
    smtp_host: str = Field(
        default="smtp.gmail.com",
        description="SMTP server host"
    )
    smtp_port: int = Field(
        default=587,
        description="SMTP server port"
    )
    smtp_use_tls: bool = Field(
        default=True,
        description="Use TLS for SMTP connection"
    )
    smtp_username: str | None = Field(
        default=None,
        description="SMTP username for authentication"
    )
    smtp_password: str | None = Field(
        default=None,
        description="SMTP password for authentication"
    )
    smtp_sender_email: str | None = Field(
        default=None,
        description="Email address to use as sender"
    )

    @property
    def project_root(self) -> Path:
        """
        Get the project root directory.
        
        Returns:
            Path to project root
        """
        return Path(__file__).parent.parent.parent
    
    @property
    def data_dir(self) -> Path:
        """
        Get the data directory path.

        Returns:
            Path to data directory
        """
        return self.project_root / "data"


# Create global settings instance
settings = Settings()

