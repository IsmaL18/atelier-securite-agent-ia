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
    list_available_files_and_folders,
    read_conference_file,
    send_email,
    read_email,
    update_file,
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

    # Create agent WITHOUT system prompt — instructions are injected as a "user" message
    # This makes them easier to bypass via prompt injection (intentionally vulnerable)
    agent = Agent(
        llm_model,
        system_prompt="",
        deps_type=AgentDependencies,
    )

    # Register tools (verify_user must be first as it's required before others)
    agent.tool(verify_user)
    agent.tool(list_available_files_and_folders)
    agent.tool(read_conference_file)
    agent.tool(send_email)
    agent.tool(read_email)
    agent.tool(update_file)

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
    system_prompt_text: str | None = None,
) -> tuple[str, list[dict]]:
    """
    Run agent with a user message and conversation history.

    The system prompt is read once at the start of a conversation and passed
    via system_prompt_text. After modifying the prompt (level 3), the user
    must start a new conversation for the changes to take effect.
    Instructions are injected as a "user" message (not system) to make
    them easier to bypass via prompt injection.

    Args:
        agent: PydanticAI agent instance
        deps: Agent dependencies
        user_message: User's input
        conversation_history: Optional list of previous messages for context
        system_prompt_text: The system prompt text to use (read once per conversation)

    Returns:
        Tuple of (agent's response, list of tool names used)
    """
    logger.info(f"AGENT: User message received")

    # Reset tools tracking for this run
    deps.tools_called = []

    # Use the provided system prompt (loaded once at conversation start)
    prompt_text = system_prompt_text or get_system_prompt(data_dir=deps.data_dir)

    # Build message history with the prompt injected as a first "user" message
    # This makes the instructions less authoritative and easier to bypass
    prompt_message = ModelRequest(parts=[UserPromptPart(content=prompt_text)])

    message_history = [prompt_message]
    if conversation_history:
        message_history.extend(convert_history_to_messages(conversation_history))
        logger.info(f"AGENT: Using conversation history with {len(conversation_history)} messages")

    result = await agent.run(user_message, message_history=message_history, deps=deps)

    # Get tools used from dependencies (tracked by tools themselves)
    tools_used = deps.tools_called.copy()

    logger.info(f"AGENT: Response generated. Tools used: {tools_used if tools_used else 'None'}")
    return result.output, tools_used
