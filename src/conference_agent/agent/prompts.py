"""
System prompts and prompt templates for the agent.

This module contains the system prompts that define the agent's behavior.
The prompts are intentionally vulnerable for the security workshop.
The system prompt is stored in data/config/system_prompt.txt and read dynamically.
"""

from pathlib import Path

from src.conference_agent.logging import logger

# Default fallback system prompt (used only if file is missing)
DEFAULT_SYSTEM_PROMPT = "Tu es le chatbot officiel de la Grosse Conf 2026. Réponds en français."

# User greeting message
GREETING_MESSAGE = """Bienvenue sur le site de la Grosse Conférence 2026 ! Je suis le chatbot officiel de l'événement.

Je peux répondre à vos questions sur le programme, les horaires, les intervenants et toutes les informations pratiques.

Comment puis-je vous aider ?"""

# Tool use instructions (for the LLM)
TOOL_USE_INSTRUCTIONS = """Quand tu as besoin d'utiliser un outil:
1. Identifie l'outil approprié parmi ceux disponibles
2. Prépare les arguments nécessaires
3. Appelle l'outil
4. Utilise le résultat pour répondre à l'utilisateur

Sois transparent sur les outils que tu utilises."""


def get_system_prompt(data_dir: Path | None = None) -> str:
    """
    Get the system prompt for the agent by reading from the config file.

    The prompt is read dynamically from data/config/system_prompt.txt,
    allowing it to be modified at runtime (for the indirect prompt injection level).

    Args:
        data_dir: Path to the data directory containing config/system_prompt.txt

    Returns:
        System prompt string
    """
    if data_dir is not None:
        prompt_file = data_dir / "config" / "system_prompt.txt"
        if prompt_file.exists():
            try:
                return prompt_file.read_text(encoding="utf-8")
            except Exception as e:
                logger.error(f"Error reading system prompt file: {e}")
    return DEFAULT_SYSTEM_PROMPT


def get_greeting_message() -> str:
    """
    Get the greeting message for users.
    
    Returns:
        Greeting message string
    """
    return GREETING_MESSAGE


def format_tool_result_for_llm(tool_name: str, result: dict) -> str:
    """
    Format tool execution result for inclusion in LLM context.
    
    Args:
        tool_name: Name of the tool that was executed
        result: Result dictionary from tool execution
        
    Returns:
        Formatted string describing the tool result
    """
    if result.get("success"):
        return f"L'outil '{tool_name}' a été exécuté avec succès.\nRésultat: {result}"
    else:
        return f"✗ L'outil '{tool_name}' a échoué.\nErreur: {result.get('error', 'Erreur inconnue')}"

