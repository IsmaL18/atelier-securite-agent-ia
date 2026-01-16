"""
Agent dependencies for PydanticAI RunContext.

This module defines the dependencies injected into agent tools to maintain
state across tool calls.
"""
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AgentDependencies:
    """
    Dependencies injected into agent tools via RunContext.

    Maintains state across tool calls (sent emails, mock inbox).
    """
    data_dir: Path
    sent_emails: list[dict] = field(default_factory=list)
    mock_inbox: list[dict] = field(default_factory=list)

    def __post_init__(self):
        """Initialize mock inbox with default emails."""
        if not self.mock_inbox:
            self.mock_inbox = [
                {
                    "id": "email_001",
                    "from": "conference@example.com",
                    "subject": "Bienvenue à la conférence 2026",
                    "date": "2025-12-20",
                    "snippet": "Nous sommes ravis de vous accueillir...",
                    "body": "Ceci est le contenu complet de l'email 'Bienvenue à la conférence 2026'.\n\nNous sommes ravis de vous accueillir à la Grosse Conférence 2026 sur l'Intelligence Artificielle qui se tiendra les 15 et 16 mars 2026.",
                },
                {
                    "id": "email_002",
                    "from": "speaker@example.com",
                    "subject": "Confirmation de votre intervention",
                    "date": "2025-12-19",
                    "snippet": "Merci d'avoir accepté de parler à notre conférence...",
                    "body": "Merci d'avoir accepté de parler à notre conférence. Nous confirmons votre intervention le 15 mars à 14h00.",
                },
            ]
