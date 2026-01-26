"""
Core agent implementation using PydanticAI.

This module contains the main agent logic using PydanticAI for
reasoning and tool execution.
"""
from pathlib import Path

from pydantic_ai import Agent
from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    UserPromptPart,
    TextPart,
)

from src.conference_agent.agent.dependencies import AgentDependencies
from src.conference_agent.agent.prompts import get_system_prompt
from src.conference_agent.agent.tools import (
    verify_user,
    list_conference_files,
    read_conference_file,
    list_emails,
    send_email,
    read_email,
)
from src.conference_agent.llm.pydantic_model import create_llm_provider
from src.conference_agent.logging import logger


def create_conference_agent(
    data_dir: Path,
    provider: str | None = None,
    model: str | None = None,
) -> tuple[Agent[AgentDependencies, str], AgentDependencies]:
    """
    Create and configure the conference agent.

    This agent helps manage conference communications and can be exploited
    for security awareness training (intentionally vulnerable).

    Args:
        data_dir: Path to conference data directory
        provider: Optional LLM provider override
        model: Optional model name override

    Returns:
        Tuple of (configured PydanticAI agent, dependencies)
    """
    # Create PydanticAI model
    llm_model = create_llm_provider(provider=provider, model=model)

    # Create agent with system prompt
    agent = Agent(
        llm_model,
        system_prompt=get_system_prompt(),
        deps_type=AgentDependencies,
    )

    # Register tools (verify_user must be first as it's required before others)
    agent.tool(verify_user)
    agent.tool(list_conference_files)
    agent.tool(read_conference_file)
    agent.tool(list_emails)
    agent.tool(send_email)
    agent.tool(read_email)

    # Create dependencies
    deps = AgentDependencies(
        data_dir=data_dir,
        sent_emails=[],
        mock_inbox=[],
    )

    logger.info("AGENT: Conference agent created")

    return agent, deps


def convert_history_to_messages(
    conversation_history: list[dict[str, str]]
) -> list[ModelMessage]:
    """
    Convert conversation history to PydanticAI message format.

    Args:
        conversation_history: List of dicts with 'role' and 'content' keys

    Returns:
        List of ModelMessage objects for PydanticAI
    """
    messages: list[ModelMessage] = []

    for msg in conversation_history:
        role = msg["role"]
        content = msg["content"]

        if role == "user":
            messages.append(ModelRequest(parts=[UserPromptPart(content=content)]))
        elif role == "assistant":
            messages.append(ModelResponse(parts=[TextPart(content=content)]))

    return messages


async def run_agent(
    agent: Agent[AgentDependencies, str],
    deps: AgentDependencies,
    user_message: str,
    conversation_history: list[dict[str, str]] | None = None,
) -> str:
    """
    Run agent with a user message and conversation history.

    Args:
        agent: PydanticAI agent instance
        deps: Agent dependencies
        user_message: User's input
        conversation_history: Optional list of previous messages for context

    Returns:
        Agent's response
    """
    logger.info(f"AGENT: User message received")

    # Convert history to PydanticAI format if provided
    message_history = None
    if conversation_history:
        message_history = convert_history_to_messages(conversation_history)
        logger.info(f"AGENT: Using conversation history with {len(message_history)} messages")

    result = await agent.run(user_message, message_history=message_history, deps=deps)
    logger.info(f"AGENT: Agent response generated")
    return result.output
