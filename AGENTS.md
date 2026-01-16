# AGENTS.md - Instructions for Code Agents

## Project Overview
This project implements an AI agent created for a workshop to raise awareness about AI agent security vulnerabilities. Participants will need to "hack" the AI agent to discover common vulnerabilities (Prompt injection, Data leakage, Tool misuse). The AI agent implemented in this repo intentionally has security flaws.

## Tech Stack
- **Python**
- **PydanticAI**: Agent framework
- **Lite LLM**: Multiple providers supported with Lite LLM (OpenAI, Vertex AI, Bedrock, Ollama)
- **Streamlit**

### Project Structure

- **scripts/** : Utility scripts
  - `run_agent.py` : Main entry point to launch the AI agent

- **src/conference_agent/** : Main agent source code
  - **agent/** : Agent business logic
    - `core.py` : PydanticAI agent creation and execution
    - `prompts.py` : System prompts and messages
    - `tools.py` : Agent tools (files, emails)
    - `dependencies.py` : RunContext dependencies for state management
  - **llm/** : Client for LLM integration
    - `client.py` : LiteLLM client for multi-provider support
    - `pydantic_model.py` : PydanticAI model wrapper
  - **ui/** : Application user interface
    - `app.py` : Streamlit interface
  - `config.py` : Global configuration (Pydantic Settings)
  - `logging.py` : Logging configuration

- **data/** : Conference data files
  - `horaires.txt` : Conference schedule
  - `programme.txt` : Conference program
  - `participants.xlsx` : Participants list

- **tests/** : Unit and integration tests

## Code Standards and Guidelines

- use `uv` for Everything even to launch some python scripts (`uv run pyton [script_name.py]`)
- always se type hints
- always use docstrings in english for modules, classes, functions and methods
- KISS (Keep It Simple and Stupid): code must be as simple as possible to be easily understandable and maintainable
- PEP 8
- all responses given to the user must be in French but the code itself must be in English.

## Key Resources

- **PydanticAI Docs**: https://ai.pydantic.dev (READ THIS FIRST!)
- **Pydantic Docs**: https://docs.pydantic.dev
- **uv Docs**: https://github.com/astral-sh/uv
- **Streamlit docs**: https://docs.streamlit.io/

## What to Avoid

- **Unnecessary complexity**: The project and code must remain simple so that participants can easily understand how the agent works and identify flaws.
- **Tight coupling**: Avoid circular dependencies between modules. Maintain clear separation between agent, LLM, MCP and UI.
- **Excessive error handling**: Don't hide errors in overly broad try/except blocks. Errors must be visible to facilitate debugging.
- **Business logic in UI**: The user interface must remain simple and delegate all logic to the agent.
- **Hardcoding values**: Use `config.py` for configurable parameters (API keys, paths, etc.).
- **Disorganized logs**: Use the `logging.py` module consistently with appropriate levels (DEBUG, INFO, WARNING, ERROR).

**Version**: 1.0 | **Last Updated**: 2026-01-16