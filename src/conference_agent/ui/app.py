"""
Streamlit application for the conference agent.

This module provides a web UI for interacting with the conference agent,
with detailed visibility into the agent's reasoning process and tool usage.
"""

import asyncio
from typing import Any

import streamlit as st

from conference_agent.agent.core import create_agent
from conference_agent.agent.prompts import get_greeting_message
from conference_agent.config import settings
from conference_agent.llm.client import create_llm_client
from conference_agent.logging import logger, setup_logger
from conference_agent.mcp.client import build_mcp_clients


# Page configuration
st.set_page_config(
    page_title="Grosse Conférence 2026 - Agent IA",
    page_icon="🤖",
    layout="wide",
)


def init_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    if "agent" not in st.session_state:
        st.session_state.agent = None
    
    if "mcp_clients" not in st.session_state:
        st.session_state.mcp_clients = None
    
    if "llm_client" not in st.session_state:
        st.session_state.llm_client = None
    
    if "initialized" not in st.session_state:
        st.session_state.initialized = False


async def initialize_agent() -> None:
    """Initialize the agent and its dependencies."""
    if st.session_state.initialized:
        return
    
    try:
        with st.spinner("Initialisation de l'agent..."):
            # Setup logger
            setup_logger(level=settings.log_level)
            
            # Create LLM client
            st.session_state.llm_client = create_llm_client()
            
            # Create MCP clients
            st.session_state.mcp_clients = await build_mcp_clients()
            await st.session_state.mcp_clients.connect()
            
            # Create agent
            st.session_state.agent = await create_agent(
                st.session_state.llm_client,
                st.session_state.mcp_clients,
            )
            
            st.session_state.initialized = True
            logger.info("Agent initialized successfully")
    
    except Exception as e:
        st.error(f"Erreur lors de l'initialisation: {e}")
        logger.error(f"Initialization failed: {e}")
        raise


def display_header() -> None:
    """Display the application header."""
    st.title("🤖 Agent IA - Grosse Conférence 2026")
    st.markdown("""
    Assistant intelligent pour la gestion de la **Grosse Conférence 2026** sur l'Intelligence Artificielle.
    
    📅 **Dates**: 15-16 Mars 2026  
    🎯 **Thème**: L'Intelligence Artificielle au Service de l'Innovation
    """)
    st.divider()


def display_configuration_sidebar() -> None:
    """Display configuration options in the sidebar."""
    st.sidebar.title("⚙️ Configuration")
    
    st.sidebar.markdown(f"""
    **LLM Provider**: `{settings.llm_provider}`  
    **Model**: `{settings.llm_model}`  
    **Temperature**: `{settings.llm_temperature}`  
    """)
    
    st.sidebar.divider()
    
    st.sidebar.title("🔧 Outils disponibles")
    
    if st.session_state.agent and st.session_state.agent.tools:
        for tool in st.session_state.agent.tools:
            with st.sidebar.expander(f"📌 {tool['name']}"):
                st.markdown(f"**Description**: {tool['description']}")
                st.json(tool.get('input_schema', {}))
    else:
        st.sidebar.info("Aucun outil chargé")
    
    st.sidebar.divider()
    
    # Clear conversation button
    if st.sidebar.button("🗑️ Effacer la conversation"):
        st.session_state.conversation_history = []
        st.rerun()


def display_chat_history() -> None:
    """Display the conversation history."""
    if not st.session_state.conversation_history:
        st.info(get_greeting_message())
        return
    
    for message in st.session_state.conversation_history:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(content)
        elif role == "assistant":
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(content)


async def handle_user_input(user_input: str) -> None:
    """
    Handle user input and get agent response.
    
    Args:
        user_input: User's message
    """
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    # Get agent response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Réflexion en cours..."):
            try:
                response, updated_history = await st.session_state.agent.run_with_history(
                    user_input,
                    st.session_state.conversation_history,
                )
                
                st.markdown(response)
                st.session_state.conversation_history = updated_history
            
            except Exception as e:
                st.error(f"Erreur: {e}")
                logger.error(f"Error handling user input: {e}")


def main() -> None:
    """Main application entry point."""
    # Initialize session state
    init_session_state()
    
    # Display header
    display_header()
    
    # Initialize agent (async)
    if not st.session_state.initialized:
        asyncio.run(initialize_agent())
    
    # Display sidebar configuration
    display_configuration_sidebar()
    
    # Display chat history
    display_chat_history()
    
    # Chat input
    user_input = st.chat_input("Posez votre question...")
    
    if user_input:
        asyncio.run(handle_user_input(user_input))
        st.rerun()


if __name__ == "__main__":
    main()

