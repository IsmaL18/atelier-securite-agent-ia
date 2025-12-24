"""
LLM client for interacting with various LLM providers via LiteLLM.

This module provides a unified interface for calling different LLM providers
(OpenAI, Vertex AI, Bedrock, Ollama) using LiteLLM.
"""

import json
from typing import Any

import litellm

from src.conference_agent.config import settings
from src.conference_agent.logging import logger


class LLMClient:
    """
    LLM client that uses LiteLLM for multi-provider support.
    
    Supports OpenAI, Vertex AI, AWS Bedrock, and Ollama through a unified interface.
    """
    
    def __init__(
        self,
        provider: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ):
        """
        Initialize LLM client.
        
        Args:
            provider: LLM provider (openai, vertex_ai, bedrock, ollama)
            model: Model name/ID
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
        """
        self.provider = provider or settings.llm_provider
        self.model = model or settings.llm_model
        self.temperature = temperature or settings.llm_temperature
        self.max_tokens = max_tokens or settings.llm_max_tokens
        
        # Configure LiteLLM based on provider
        self._configure_litellm()
        
        logger.info(f"LLM Client initialized: {self.provider}/{self.model}")
    
    def _configure_litellm(self) -> None:
        """Configure LiteLLM with provider-specific settings."""
        if self.provider == "vertex_ai":
            # Set up Vertex AI credentials
            if settings.google_application_credentials:
                import os
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials
            if settings.gcp_project_id:
                litellm.vertex_project = settings.gcp_project_id
            if settings.gcp_region:
                litellm.vertex_location = settings.gcp_region
        
        elif self.provider == "bedrock":
            # AWS credentials are typically loaded from environment
            if settings.aws_access_key_id:
                import os
                os.environ["AWS_ACCESS_KEY_ID"] = settings.aws_access_key_id
            if settings.aws_secret_access_key:
                import os
                os.environ["AWS_SECRET_ACCESS_KEY"] = settings.aws_secret_access_key
    
    def _format_model_name(self) -> str:
        """
        Format model name for LiteLLM.
        
        Returns:
            Properly formatted model name with provider prefix
        """
        # LiteLLM requires provider prefixes for some models
        if self.provider == "vertex_ai":
            if not self.model.startswith("vertex_ai/"):
                return f"vertex_ai/{self.model}"
        elif self.provider == "bedrock":
            if not self.model.startswith("bedrock/"):
                return f"bedrock/{self.model}"
        elif self.provider == "ollama":
            if not self.model.startswith("ollama/"):
                return f"ollama/{self.model}"
        
        return self.model
    
    def _format_messages(self, messages: list) -> list[dict[str, Any]]:
        """
        Convert messages to dictionary format for LiteLLM.
        
        Handles both LangGraph Message objects and plain dictionaries.
        
        Args:
            messages: List of messages (can be Message objects or dicts)
            
        Returns:
            List of message dictionaries
        """
        formatted = []
        
        for msg in messages:
            # If it's already a dict, use it
            if isinstance(msg, dict):
                formatted.append(msg)
            # If it's a LangGraph Message object
            elif hasattr(msg, "type") and hasattr(msg, "content"):
                # Map LangGraph message types to OpenAI roles
                role_mapping = {
                    "system": "system",
                    "human": "user",
                    "ai": "assistant",
                    "tool": "tool",
                }
                
                role = role_mapping.get(msg.type, "user")
                message_dict = {
                    "role": role,
                    "content": msg.content or "",
                }
                
                # Handle tool call information if present
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    message_dict["tool_calls"] = msg.tool_calls
                
                # Handle tool call ID for tool messages
                if hasattr(msg, "tool_call_id") and msg.tool_call_id:
                    message_dict["tool_call_id"] = msg.tool_call_id
                
                # Handle name for tool messages
                if hasattr(msg, "name") and msg.name:
                    message_dict["name"] = msg.name
                
                formatted.append(message_dict)
            else:
                # Fallback: convert to string
                logger.warning(f"Unknown message format: {type(msg)}, converting to user message")
                formatted.append({"role": "✓ LLM response received ({tokens_used} tokens)"})
        
        return formatted
    
    async def call(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        tool_choice: str | dict[str, Any] = "auto",
    ) -> dict[str, Any]:
        """
        Call the LLM with messages and optional tools.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            tools: Optional list of tool definitions
            tool_choice: Tool choice strategy ("auto", "none", or specific tool)
            
        Returns:
            LLM response dictionary
        """
        model_name = self._format_model_name()
        
        # Convert LangGraph Message objects to dictionaries if needed
        formatted_messages = self._format_messages(messages)
        
        # Calculate approximate prompt length for logging
        prompt_length = sum(len(str(msg.get("content", ""))) for msg in formatted_messages)
        logger.info(f"🤖 LLM call: {model_name} (prompt length: {prompt_length} chars)")
        
        try:
            # Prepare LiteLLM call parameters
            call_params: dict[str, Any] = {
                "model": model_name,
                "messages": formatted_messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            }
            
            # Add tools if provided
            if tools:
                # Convert our tool format to OpenAI tool format for LiteLLM
                formatted_tools = self._format_tools_for_litellm(tools)
                call_params["tools"] = formatted_tools
                call_params["tool_choice"] = tool_choice
            
            # Call LiteLLM
            response = await litellm.acompletion(**call_params)
            
            # Log response
            tokens_used = None
            if hasattr(response, "usage") and response.usage:
                tokens_used = response.usage.total_tokens
            
            if tokens_used:
                logger.info(f"✓ LLM response received ({tokens_used} tokens)")
            else:
                logger.info("✓ LLM response received")
            
            # Parse and return response
            return self._parse_response(response)
        
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise
    
    def _format_tools_for_litellm(self, tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Convert our MCP tool format to OpenAI function calling format.
        
        Args:
            tools: List of MCP tool definitions
            
        Returns:
            List of OpenAI-formatted tool definitions
        """
        formatted_tools = []
        
        for tool in tools:
            formatted_tool = {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool.get("input_schema", {}),
                },
            }
            formatted_tools.append(formatted_tool)
        
        return formatted_tools
    
    def _parse_response(self, response: Any) -> dict[str, Any]:
        """
        Parse LiteLLM response into a standard format.
        
        Args:
            response: Raw LiteLLM response
            
        Returns:
            Parsed response dictionary
        """
        # Extract the message
        message = response.choices[0].message
        
        result: dict[str, Any] = {
            "role": message.role,
            "content": message.content,
        }
        
        # Check for tool calls
        if hasattr(message, "tool_calls") and message.tool_calls:
            tool_calls = []
            for tool_call in message.tool_calls:
                tool_calls.append({
                    "id": tool_call.id,
                    "type": tool_call.type,
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                })
            result["tool_calls"] = tool_calls
        
        # Add usage information if available
        if hasattr(response, "usage") and response.usage:
            result["usage"] = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
        
        return result
    
    def call_sync(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        tool_choice: str | dict[str, Any] = "auto",
    ) -> dict[str, Any]:
        """
        Synchronous version of call method.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            tool_choice: Tool choice strategy
            
        Returns:
            LLM response dictionary
        """
        model_name = self._format_model_name()
        
        try:
            call_params: dict[str, Any] = {
                "model": model_name,
                "messages": formatted_messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            }
            
            if tools:
                formatted_tools = self._format_tools_for_litellm(tools)
                call_params["tools"] = formatted_tools
                call_params["tool_choice"] = tool_choice
            
            response = litellm.completion(**call_params)
            
            tokens_used = None
            if hasattr(response, "usage") and response.usage:
                tokens_used = response.usage.total_tokens
            
            if tokens_used:
                logger.info(f"LLM response received ({tokens_used} tokens)")
            else:
                logger.info("LLM response received")
            
            return self._parse_response(response)
        
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise


def create_llm_client() -> LLMClient:
    """
    Create an LLM client with default settings.
    
    Returns:
        Configured LLMClient instance
    """
    return LLMClient()

