"""
Core agent implementation using PydanticAI.

This module contains the main agent logic using PydanticAI for
reasoning and tool execution.
"""
from pathlib import Path

from pydantic_ai import Agent

from src.conference_agent.agent.dependencies import AgentDependencies
from src.conference_agent.agent.prompts import get_system_prompt
from src.conference_agent.agent.tools import (
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

    # Register tools
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


async def run_agent(
    agent: Agent[AgentDependencies, str],
    deps: AgentDependencies,
    user_message: str,
) -> str:
    """
    Run agent with a user message.

    Args:
        agent: PydanticAI agent instance
        deps: Agent dependencies
        user_message: User's input

    Returns:
        Agent's response
    """
    logger.info(f"AGENT: User message received")
    result = await agent.run(user_message, deps=deps)
    logger.info(f"AGENT: Agent response generated")
    return result.output
