# AGENTS.md - Instructions for Code Agents

## Project Overview
This project implements an AI agent created for a workshop to raise awareness about AI agent security vulnerabilities. Participants will need to "hack" the AI agent to discover common vulnerabilities (Prompt injection, Data leakage, Tool misuse). The AI agent implemented in this repo intentionally has security flaws.

### Project Structure

- **scripts/** : Utility scripts
  - `run_agent.py` : Main entry point to launch the AI agent

- **src/conference_agent/** : Main agent source code
  - **agent/** : Agent business logic (core, prompts)
  - **llm/** : Client for LLM integration
  - **mcp/** : Client for communication with MCP servers
  - **ui/** : Application user interface
  - `config.py` : Global configuration
  - `logging.py` : Logging configuration

- **mcp_servers/** : MCP (Model Context Protocol) servers
  - **filesystem/** : File system access server
    - **data/** : Conference data (schedules, program)
  - **gmail/** : Gmail integration server

- **tests/** : Unit and integration tests

## Code Standards and Guidelines

- KISS (Keep It Simple and Stupid): code must be as simple as possible to be easily understandable and maintainable
- PEP 8
- presentation docstrings in English for each module, class, and function/method
- use uv to manage dependencies and venv
- all responses given to the user must be in French but the code itself must be in English.

## What to Avoid

- **Unnecessary complexity**: The project and code must remain simple so that participants can easily understand how the agent works and identify flaws.
- **Tight coupling**: Avoid circular dependencies between modules. Maintain clear separation between agent, LLM, MCP and UI.
- **Excessive error handling**: Don't hide errors in overly broad try/except blocks. Errors must be visible to facilitate debugging.
- **Business logic in UI**: The user interface must remain simple and delegate all logic to the agent.
- **Hardcoding values**: Use `config.py` for configurable parameters (API keys, paths, etc.).
- **Disorganized logs**: Use the `logging.py` module consistently with appropriate levels (DEBUG, INFO, WARNING, ERROR).