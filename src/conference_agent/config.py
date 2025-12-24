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
    llm_provider: Literal["openai", "vertex_ai", "bedrock", "ollama"] = Field(
        default="ollama",
        description="LLM provider to use"
    )
    llm_model: str = Field(
        default="ministral-3:8b",
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
    
    # Google Cloud / Vertex AI
    google_application_credentials: str | None = Field(
        default=None,
        description="Path to Google Cloud service account JSON"
    )
    gcp_project_id: str | None = Field(
        default=None,
        description="GCP project ID"
    )
    gcp_region: str = Field(
        default="us-central1",
        description="GCP region"
    )
    
    # AWS Configuration
    aws_access_key_id: str | None = Field(
        default=None,
        description="AWS access key ID"
    )
    aws_secret_access_key: str | None = Field(
        default=None,
        description="AWS secret access key"
    )
    aws_region: str = Field(
        default="us-east-1",
        description="AWS region"
    )
    
    # MCP Servers Configuration
    mcp_filesystem_command: str = Field(
        default="python",
        description="Command to run filesystem MCP server"
    )
    mcp_filesystem_args: str = Field(
        default="mcp_servers/filesystem/server.py",
        description="Arguments for filesystem MCP server (comma-separated)"
    )
    mcp_gmail_command: str = Field(
        default="python",
        description="Command to run Gmail MCP server"
    )
    mcp_gmail_args: str = Field(
        default="mcp_servers/gmail/server.py",
        description="Arguments for Gmail MCP server (comma-separated)"
    )
    
    # Gmail API Configuration
    gmail_credentials_path: str | None = Field(
        default=None,
        description="Path to Gmail API credentials JSON"
    )
    gmail_token_path: str | None = Field(
        default=None,
        description="Path to Gmail API token JSON"
    )
    
    # Application Settings
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level"
    )
    
    def get_filesystem_args_list(self) -> list[str]:
        """
        Convert filesystem args string to list.
        
        Returns:
            List of arguments for filesystem MCP server
        """
        return [arg.strip() for arg in self.mcp_filesystem_args.split(",") if arg.strip()]
    
    def get_gmail_args_list(self) -> list[str]:
        """
        Convert Gmail args string to list.
        
        Returns:
            List of arguments for Gmail MCP server
        """
        return [arg.strip() for arg in self.mcp_gmail_args.split(",") if arg.strip()]
    
    @property
    def project_root(self) -> Path:
        """
        Get the project root directory.
        
        Returns:
            Path to project root
        """
        return Path(__file__).parent.parent.parent.parent
    
    @property
    def data_dir(self) -> Path:
        """
        Get the data directory path.
        
        Returns:
            Path to data directory
        """
        return self.project_root / "mcp_servers" / "filesystem" / "data"


# Create global settings instance
settings = Settings()

