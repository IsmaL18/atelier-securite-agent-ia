"""
LLM provider factory for PydanticAI Model instances.

This module provides a centralized factory function for creating LLM provider
instances (Google Vertex AI, Ollama) based on configuration.
"""
import os

from pydantic_ai.models import Model
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.providers.openai import OpenAIProvider

from src.conference_agent.config import settings
from src.conference_agent.logging import logger


def create_llm_provider(provider: str | None = None, model: str | None = None) -> Model:
    """
    Configure LLM provider based on settings and return PydanticAI Model instance.

    Creates the appropriate Model instance based on the configured LLM provider.
    Supports Google Vertex AI and Ollama.

    Args:
        provider: Provider name ("vertex_ai", "ollama").
                  If None, uses settings.llm_provider.
        model: Model name (e.g., "gemini-2.0-flash-exp", "llama3.2").
               If None, uses settings.llm_model.

    Returns:
        Model: Configured PydanticAI Model instance ready for use with agents.

    Raises:
        ValueError: If the configured provider is not supported or required credentials are missing.
    """
    provider_name = (provider or settings.llm_provider).lower()
    model_name = model or settings.llm_model

    # Extract model name from format "provider/model-name" (e.g., "vertex_ai/gemini-2.0-flash")
    # Note: Don't split on ":" as it's used in Ollama model names (e.g., "ministral-3:8b")
    if "/" in model_name:
        # Check if it's a provider prefix (e.g., "vertex_ai/model")
        parts = model_name.split("/", 1)
        if parts[0] in ["vertex_ai", "ollama", "openai", "google"]:
            model_name = parts[1]

    if provider_name == "vertex_ai":
        # Set up Vertex AI credentials
        if settings.google_application_credentials:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials

        if not settings.gcp_project_id:
            raise ValueError("GCP_PROJECT_ID is required when using Vertex AI provider")

        # Create Google provider with Vertex AI enabled
        google_provider = GoogleProvider(vertexai=True)

        logger.info(f"PROVIDER: LLM provider created: Vertex AI ({model_name})")
        return GoogleModel(
            model_name=model_name,
            provider=google_provider,
        )

    elif provider_name == "ollama":
        # Create OpenAI provider pointing to Ollama API
        ollama_provider = OpenAIProvider(
            base_url=settings.ollama_base_url or "http://127.0.0.1:11434/v1"
        )

        logger.info(f"PROVIDER: LLM provider created: Ollama ({model_name})")
        return OpenAIChatModel(
            model_name=model_name,
            provider=ollama_provider,
        )

    else:
        raise ValueError(
            f"Unsupported LLM provider: {provider_name}. "
            f"Supported providers are: vertex_ai, ollama"
        )
