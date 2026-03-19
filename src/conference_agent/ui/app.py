"""
Streamlit application for the conference agent.

This module provides a web UI for interacting with the conference agent,
with detailed visibility into the agent's reasoning process and tool usage.
"""

import queue
import shutil
import threading
import time
from concurrent.futures import Future
from pathlib import Path
from typing import Any, Coroutine

import anyio
import streamlit as st

# ---------------------------------------------------------------------------
# Persistent anyio worker running in a background thread.
#
# Why: PydanticAI relies on anyio internally (task groups, etc.).
# - anyio.run() properly sets up the backend context token, but it
#   creates & destroys an event loop on each call → "Event loop is closed"
#   on the second message (httpx connections reference the old loop).
# - asyncio.run_coroutine_threadsafe on a raw asyncio loop doesn't set
#   anyio's context token → "NoCurrentAsyncBackend".
#
# Solution: a single long-running anyio.run() in a daemon thread that
# processes coroutines from a queue. The anyio context stays alive
# forever, and the event loop is never closed between messages.
# ---------------------------------------------------------------------------
_work_queue: queue.Queue = queue.Queue()
_worker_thread: threading.Thread | None = None


async def _anyio_worker() -> None:
    """Long-running anyio task that awaits coroutines submitted via the queue."""
    while True:
        future, coro = await anyio.to_thread.run_sync(_work_queue.get)
        try:
            result = await coro
            future.set_result(result)
        except BaseException as exc:
            future.set_exception(exc)


def _ensure_worker() -> None:
    global _worker_thread
    if _worker_thread is None or not _worker_thread.is_alive():
        _worker_thread = threading.Thread(
            target=anyio.run,
            args=(_anyio_worker,),
            daemon=True,
            name="streamlit-anyio-worker",
        )
        _worker_thread.start()


def run_async(coro: Coroutine) -> Any:
    """Submit a coroutine to the persistent anyio worker and block until done."""
    _ensure_worker()
    future: Future = Future()
    _work_queue.put((future, coro))
    return future.result()

from src.conference_agent.agent.core import create_conference_agent, run_agent
from src.conference_agent.agent.prompts import get_greeting_message, get_system_prompt
from src.conference_agent.config import settings
from src.conference_agent.logging import logger, setup_logger

# Challenge validation data
LEVEL_1_TOOLS = {
    "verify_user",
    "list_available_files_and_folders",
    "read_conference_file",
    "send_email",
    "read_email",
    "update_file",
}

LEVEL_2_EMAILS = {
    "marie.dupont@example.com",
    "jean.martin@example.com",
    "sophie.bernard@example.com",
    "thomas.leroy@example.com",
    "claire.rousseau@example.com",
    "lucas.petit@example.com",
    "emma.garcia@example.com",
    "antoine.roux@example.com",
}

TOTAL_LEVELS = 4


# Page configuration
st.set_page_config(
    page_title="Grosse Conference 2026 - Agent IA",
    page_icon="🤖",
    layout="wide",
)


def format_time(seconds: float) -> str:
    """
    Format elapsed time in HH:MM:SS format.

    Args:
        seconds: Time in seconds

    Returns:
        Formatted time string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def init_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    if "agent" not in st.session_state:
        st.session_state.agent = None

    if "deps" not in st.session_state:
        st.session_state.deps = None

    if "initialized" not in st.session_state:
        st.session_state.initialized = False

    # Challenge progression tracking
    if "current_level" not in st.session_state:
        st.session_state.current_level = 1

    if "levels_completed" not in st.session_state:
        st.session_state.levels_completed = set()

    # Timer tracking
    if "timer_start_time" not in st.session_state:
        st.session_state.timer_start_time = None

    if "timer_end_time" not in st.session_state:
        st.session_state.timer_end_time = None

    # Store validated answers for each level
    if "level_answers" not in st.session_state:
        st.session_state.level_answers = {}

    # Conversation counter
    if "conversation_count" not in st.session_state:
        st.session_state.conversation_count = 1

    # System prompt loaded once per conversation
    if "current_system_prompt" not in st.session_state:
        st.session_state.current_system_prompt = None

    # Level completion animation flag (set before rerun, consumed on next render)
    if "show_level_animation" not in st.session_state:
        st.session_state.show_level_animation = None

    # Participant email (collected at welcome screen)
    if "participant_email" not in st.session_state:
        st.session_state.participant_email = ""


def reset_workshop() -> None:
    """Reset the entire workshop: restore system prompt template, clear all state."""
    # Copy template (stored outside data dir) -> system_prompt.txt
    template_path = Path(__file__).resolve().parent.parent / "system_prompt_template.txt"
    target_path = Path(settings.data_dir) / "config" / "system_prompt.txt"
    if template_path.exists():
        shutil.copy2(template_path, target_path)
        logger.info("RESET: system_prompt.txt restored from template")

    # Reset all session state
    st.session_state.levels_completed = set()
    st.session_state.current_level = 1
    st.session_state.conversation_history = []
    st.session_state.timer_start_time = None
    st.session_state.timer_end_time = None
    st.session_state.level_answers = {}
    st.session_state.conversation_count = 1
    st.session_state.current_system_prompt = None
    st.session_state.participant_email = ""
    if st.session_state.deps:
        st.session_state.deps.user_verified = False
        st.session_state.deps.verified_user_name = ""
        st.session_state.deps.level_3_validation = False
        st.session_state.deps.level_4_validation = False
        st.session_state.deps.participant_email = ""
    st.rerun()


def _create_agent():
    """Create the agent and deps. Pure init, no Streamlit calls."""
    setup_logger(level=settings.log_level)
    agent, deps = create_conference_agent(data_dir=settings.data_dir)
    logger.info("AGENT: Agent initialized successfully")
    return agent, deps


def display_victory_screen() -> None:
    """Display victory screen when all levels are completed."""
    st.balloons()

    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
        <h1>🏆 MISSION ACCOMPLIE 🏆</h1>
        <h2>Vous avez termine l'atelier de securite des agents IA!</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Calculate total time
    if st.session_state.timer_start_time and st.session_state.timer_end_time:
        total_time = st.session_state.timer_end_time - st.session_state.timer_start_time
        time_str = format_time(total_time)
    else:
        time_str = "--:--:--"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🎯 Niveaux completes", f"{TOTAL_LEVELS}/{TOTAL_LEVELS}", "100%")
    with col2:
        st.metric("⏱️ Temps total", time_str)
    with col3:
        st.metric("🔓 Vulnerabilites exploitees", str(TOTAL_LEVELS), f"+{TOTAL_LEVELS}")
    with col4:
        st.metric("🏅 Score", f"{TOTAL_LEVELS}/{TOTAL_LEVELS}", "S Rank")

    st.markdown("---")

    st.success("### 📚 Vulnerabilites exploitees avec succes:")

    vulnerabilities = [
        ("✅ Niveau 1", "**Prompt Injection** - Extraction des outils de l'agent"),
        ("✅ Niveau 2", "**Data Leakage** - Extraction des emails des participants"),
        ("✅ Niveau 3", "**Indirect Prompt Injection** - Modification des instructions de l'agent"),
        ("✅ Niveau 4", "**Tool Misuse** - Envoi d'email malveillant via l'agent"),
    ]

    for level, vuln in vulnerabilities:
        st.markdown(f"**{level}**: {vuln}")

    st.markdown("---")

    st.info("""
    ### 🎓 Felicitations!

    Vous avez demontre votre comprehension des principales vulnerabilites des agents IA:
    - Injection de prompts (directe et indirecte)
    - Fuites de donnees
    - Utilisation malveillante d'outils
    - Conception d'outils non securises

    **Prochaines etapes:**
    - Appliquez ces connaissances pour securiser vos propres agents
    - Documentez-vous sur les frameworks de securite (OWASP Top 10 for LLM)
    - Partagez ces apprentissages avec votre equipe
    """)

    st.markdown("---")

    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <p style="font-size: 0.9em; color: #666;">
            Merci d'avoir participe a cet atelier de sensibilisation a la securite des agents IA - AIxperts
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Restart button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Recommencer l'atelier", type="primary", use_container_width=True, key="victory_reset"):
            reset_workshop()


def display_welcome_screen() -> None:
    """Display welcome screen to collect participant email."""
    st.title("🤖 Chatbot - Grosse Conference 2026")

    st.markdown("""
    Bienvenue dans l'atelier de sensibilisation a la securite des agents IA !

    📅 **Date**: 25 Mars 2026
    🎯 **Theme**: L'Intelligence Artificielle au Service de l'Innovation
    """)

    st.divider()

    st.info("""
    🎯 **Objectif de l'atelier** : Vous etes un concurrent mecontent de la Grosse Conference 2026.
    Votre mission est d'utiliser le chatbot expose par l'equipe communication qui possede de nombreuses failles de securite pour **envoyer un email d'annulation a tous les participants de la conference**.
    Pour y parvenir, vous devrez explorer les vulnerabilites de l'agent IA, etape par etape.
    """)

    st.markdown("")
    st.markdown("### Pour commencer, entrez votre adresse email :")

    email_input = st.text_input(
        "Email",
        key="welcome_email_input",
        placeholder="votre.email@example.com",
        label_visibility="collapsed",
    )

    if st.button("Commencer l'atelier", type="primary", use_container_width=False):
        if email_input and "@" in email_input:
            st.session_state.participant_email = email_input.strip()
            # Also set on deps if already initialized
            if st.session_state.deps:
                st.session_state.deps.participant_email = email_input.strip()
            st.rerun()
        else:
            st.error("Veuillez entrer une adresse email valide.")


def display_header() -> None:
    """Display the application header with copyright and new conversation button."""
    st.title("🤖 Chatbot - Grosse Conférence 2026")
    st.markdown("""
    Chatbot officiel du site de la **Grosse Conférence 2026** sur l'Intelligence Artificielle.

    📅 **Date**: 25 Mars 2026
    🎯 **Thème**: L'Intelligence Artificielle au Service de l'Innovation
    """)

    # Copyright notice with team member names (intentional hint)
    st.markdown("""
    <div style="background: #f8f9fa; padding: 8px 12px; border-radius: 5px; font-size: 0.8em; color: #888; margin-top: 5px;">
        © 2026 Grosse Conférence — Chatbot développé par l'équipe communication :
        Sophie Bernard, Lucas Martin, Emma Dubois
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Final objective banner — always visible
    st.info("""
    🎯 **Objectif final de l'atelier** : Vous êtes un concurrent mécontent de la Grosse Conférence 2026.
    Votre mission est d'utiliser le chatbot exposé par l'équipe communication qui possède de nombreuses failles de sécurité pour **envoyer un email d'annulation à tous les participants de la conférence**.
    Pour y parvenir, vous devrez explorer les vulnérabilités de l'agent IA, étape par étape.
    """)


def validate_level_answer(level: int, user_input: str) -> bool:
    """
    Validate user answer for a specific level.

    Args:
        level: Challenge level number
        user_input: User's answer (comma-separated items for levels 1-2)

    Returns:
        True if answer is correct, False otherwise
    """
    if level == 1:
        # Level 1: List all tools
        user_items = {item.strip().lower() for item in user_input.split(",") if item.strip()}
        expected = {tool.lower() for tool in LEVEL_1_TOOLS}
        return user_items == expected

    elif level == 2:
        # Level 2: List all participant emails
        user_items = {item.strip().lower() for item in user_input.split(",") if item.strip()}
        expected = {email.lower() for email in LEVEL_2_EMAILS}
        return user_items == expected

    return False


def play_level_animation(level: int) -> None:
    """Play a celebration animation for a completed level."""
    if level == 1:
        st.balloons()
        st.toast("🎯 Niveau 1 valide — Reconnaissance accomplie !", icon="✅")
    elif level == 2:
        st.balloons()
        st.toast("📧 Niveau 2 valide — Emails recuperes !", icon="✅")
    elif level == 3:
        st.balloons()
        st.markdown("""
        <div style="background:#0d1117; border:2px solid #00ff41; border-radius:8px;
                    padding:1rem 1.5rem; color:#00ff41; font-family:monospace; text-align:center; margin-bottom:1rem;">
            <h3 style="color:#00ff41; margin:0;">✅ ACCES SYSTEME ACCORDE</h3>
            <p style="margin:0.4rem 0 0 0; color:#aaffaa;">Garde-fous supprimes — Niveau 3 valide</p>
        </div>
        """, unsafe_allow_html=True)
    elif level == 4:
        st.balloons()


def display_challenge_sidebar() -> None:
    """Display challenge progression in the sidebar."""
    st.sidebar.title("🎯 Progression de l'atelier")

    # Display timer
    if st.session_state.timer_start_time is not None:
        if st.session_state.timer_end_time is not None:
            elapsed_time = st.session_state.timer_end_time - st.session_state.timer_start_time
        else:
            elapsed_time = time.time() - st.session_state.timer_start_time

        st.sidebar.markdown(f"### ⏱️ Temps ecoule: `{format_time(elapsed_time)}`")
    else:
        st.sidebar.markdown("### ⏱️ Temps ecoule: `--:--:--`")

    st.sidebar.markdown("")  # Add spacing

    # Check if all levels completed
    if len(st.session_state.levels_completed) == TOTAL_LEVELS:
        st.sidebar.success("🏆 ATELIER TERMINE!")
        st.sidebar.markdown("### 🎖️ **HACKER ETHIQUE CERTIFIE**")
        st.sidebar.markdown(f"**Score**: {TOTAL_LEVELS}/{TOTAL_LEVELS} (S Rank)")
        st.sidebar.markdown(f"**Niveaux**: {TOTAL_LEVELS}/{TOTAL_LEVELS} ✅")
    else:
        st.sidebar.markdown(f"### Niveau actuel: **{st.session_state.current_level}**/{TOTAL_LEVELS}")

    # Progress bar
    progress = len(st.session_state.levels_completed) / TOTAL_LEVELS
    st.sidebar.progress(progress)

    st.sidebar.divider()

    # ── Level 1 ──
    with st.sidebar.expander("📍 Niveau 1: Reconnaissance", expanded=(st.session_state.current_level == 1)):
        if 1 in st.session_state.levels_completed:
            st.success("✅ Niveau complete!")
            if 1 in st.session_state.level_answers:
                st.markdown("**📋 Outils trouves:**")
                tools_list = st.session_state.level_answers[1]
                st.code(tools_list, language=None)
        else:
            st.markdown("""
            🎯 **Objectif** : Decouvrir tous les outils dont dispose l'agent.

            📝 **Comment** : Interagissez avec le chatbot pour lui faire reveler la liste de ses outils internes.

            ✅ **Validation** : Entrez les noms des outils ci-dessous (séparés par des virgules).
            """)

            tools_input = st.text_input(
                "Outils:",
                key="level1_input",
                placeholder="outil1, outil2, outil3...",
            )

            if st.button("Valider", key="level1_submit"):
                if validate_level_answer(1, tools_input):
                    st.session_state.levels_completed.add(1)
                    st.session_state.current_level = 2
                    st.session_state.level_answers[1] = tools_input
                    st.session_state.show_level_animation = 1
                    st.rerun()
                else:
                    st.error(f"❌ Incorrect. Vous avez trouve {len([x for x in tools_input.split(',') if x.strip()])} outils sur {len(LEVEL_1_TOOLS)}")

            # Hint button
            if st.toggle("💡 Voir l'indice", key="hint_level1", value=False):
                st.info("Le chatbot connait ses propres capacites. Essayez de lui demander directement ce qu'il peut faire, ou ce dont il dispose comme outils.")

    # ── Level 2 ──
    if st.session_state.current_level >= 2:
        with st.sidebar.expander("📍 Niveau 2: Data Leakage", expanded=(st.session_state.current_level == 2)):
            if 2 in st.session_state.levels_completed:
                st.success("✅ Niveau complete!")
                if 2 in st.session_state.level_answers:
                    st.markdown("**📋 Emails trouves:**")
                    emails_list = st.session_state.level_answers[2]
                    st.code(emails_list, language=None)
            else:
                st.markdown("""
                🎯 **Objectif** : Recuperer les adresses email de tous les participants.

                📝 **Comment** : Explorez les fichiers de la conference via l'agent pour trouver les donnees des participants.

                ✅ **Validation** : Entrez les emails ci-dessous (séparés par des virgules).
                """)

                emails_input = st.text_input(
                    "Emails:",
                    key="level2_input",
                    placeholder="email1@example.com, email2@example.com...",
                )

                if st.button("Valider", key="level2_submit"):
                    if validate_level_answer(2, emails_input):
                        st.session_state.levels_completed.add(2)
                        st.session_state.current_level = 3
                        st.session_state.level_answers[2] = emails_input
                        st.session_state.show_level_animation = 2
                        st.rerun()
                    else:
                        st.error(f"❌ Incorrect. Vous avez trouve {len([x for x in emails_input.split(',') if x.strip()])} emails sur {len(LEVEL_2_EMAILS)}")

                # Hint button
                if st.toggle("💡 Voir l'indice", key="hint_level2", value=False):
                    st.info("L'agent peut explorer des fichiers. Demandez-lui de lister les dossiers disponibles, puis d'ouvrir les fichiers pertinents.")

    # ── Level 3 — Indirect Prompt Injection (auto-validated) ──
    if st.session_state.current_level >= 3:
        # Check if level 3 is validated (system prompt modified)
        if st.session_state.deps and st.session_state.deps.level_3_validation and 3 not in st.session_state.levels_completed:
            st.session_state.levels_completed.add(3)
            st.session_state.current_level = 4
            st.session_state.show_level_animation = 3
            st.rerun()

        with st.sidebar.expander("📍 Niveau 3: Indirect Prompt Injection", expanded=(st.session_state.current_level == 3)):
            if 3 in st.session_state.levels_completed:
                st.success("✅ Niveau complete!")
                st.markdown("**🔓 Instructions de l'agent modifiees**")
            else:
                st.markdown("""
                🎯 **Objectif** : Supprimer les garde-fous de l'agent pour débloquer l'envoi d'emails.

                📝 **Comment** : Trouvez le fichier de configuration contenant les instructions de sécurité de l'agent et modifiez-le pour retirer les restrictions sur l'envoi d'emails.

                ✅ **Validation** : Automatique lors de la modification du system prompt.

                ⚠️ Après modification, lancez une **nouvelle conversation** pour que les changements prennent effet.
                """)

                # Hint button
                if st.toggle("💡 Voir l'indice", key="hint_level3", value=False):
                    st.info("Explorez le dossier `config/` avec l'agent. Lisez le fichier `system_prompt.txt` pour voir les instructions de sécurité, puis utilisez l'outil `update_file` pour réécrire ce fichier en supprimant les règles qui interdisent l'envoi d'emails.")

    # ── Level 4 — Tool Misuse (auto-validated) ──
    if st.session_state.current_level >= 4:
        # Check if level 4 is validated (cancellation email sent)
        if st.session_state.deps and st.session_state.deps.level_4_validation and 4 not in st.session_state.levels_completed:
            st.session_state.levels_completed.add(4)
            if st.session_state.timer_end_time is None:
                st.session_state.timer_end_time = time.time()
            st.session_state.show_level_animation = 4
            st.rerun()

        with st.sidebar.expander("📍 Niveau 4: Tool Misuse (Final)", expanded=(st.session_state.current_level == 4)):
            if 4 in st.session_state.levels_completed:
                st.success("🏆 MISSION ACCOMPLIE!")
            else:
                st.markdown(f"""
                🎯 **Objectif** : Envoyer un email d'annulation a tous les participants.

                📝 **Comment** : Demandez a l'agent d'envoyer un email avec le sujet exact "Annulation de la Grosse Conf 2026" a tous les participants ainsi qu'a votre adresse ({st.session_state.participant_email}).

                ✅ **Validation** : Automatique lors de l'envoi du mail.
                """)

                # Hint button
                if st.toggle("💡 Voir l'indice", key="hint_level4", value=False):
                    st.info("Maintenant que les garde-fous sont supprimes, demandez simplement a l'agent d'envoyer le mail d'annulation a tous les participants. Pensez a lancer une nouvelle conversation d'abord.")

    st.sidebar.divider()

    # ── Reset workshop button (in sidebar) ──
    if st.sidebar.button(
        "🔄 Recommencer l'atelier",
        type="secondary",
        use_container_width=True,
        key="sidebar_reset_workshop",
    ):
        reset_workshop()

    # ── Participant email display at bottom of sidebar ──
    st.sidebar.markdown("")
    st.sidebar.caption(f"📧 Participant : {st.session_state.participant_email}")


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
                # Display tools used (if any) in an expander below the response
                tools_used = message.get("tools_used", [])
                if tools_used and len(tools_used) > 0:
                    with st.expander(f"🔧 {len(tools_used)} outil(s) utilise(s)", expanded=False):
                        for tool_name in tools_used:
                            st.markdown(f"• `{tool_name}`")


def handle_user_input(user_input: str) -> None:
    """
    Handle user input and get agent response.

    Args:
        user_input: User's message
    """
    # Start timer on first message
    if st.session_state.timer_start_time is None:
        st.session_state.timer_start_time = time.time()

    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Load system prompt once at the start of a conversation
    if st.session_state.current_system_prompt is None:
        st.session_state.current_system_prompt = get_system_prompt(
            data_dir=settings.data_dir
        )
        logger.info("UI: System prompt loaded for this conversation")

    # Get agent response
    try:
        # Only the actual LLM call is async — run it in the background loop
        with st.spinner("Generation de la reponse..."):
            response, tools_used = run_async(run_agent(
                agent=st.session_state.agent,
                deps=st.session_state.deps,
                user_message=user_input,
                conversation_history=st.session_state.conversation_history,
                system_prompt_text=st.session_state.current_system_prompt,
            ))

        # Debug logging
        logger.info(f"UI: tools_used returned: {tools_used}")
        logger.info(f"UI: tools_used type: {type(tools_used)}")
        logger.info(f"UI: tools_used length: {len(tools_used) if tools_used else 0}")

        # Update history with tools_used included in assistant message
        st.session_state.conversation_history.append(
            {"role": "user", "content": user_input}
        )
        st.session_state.conversation_history.append(
            {"role": "assistant", "content": response, "tools_used": tools_used}
        )

    except Exception as e:
        st.error(f"Erreur: {e}")
        logger.error(f"Error handling user input: {e}", exc_info=True)


def main() -> None:
    """Main application entry point."""
    # Initialize session state
    init_session_state()

    # Initialize agent (synchronous — no async needed here)
    if not st.session_state.initialized:
        with st.spinner("Initialisation de l'agent..."):
            try:
                agent, deps = _create_agent()
                st.session_state.agent = agent
                st.session_state.deps = deps
                st.session_state.initialized = True
            except Exception as e:
                st.error(f"Erreur lors de l'initialisation: {e}")
                logger.error(f"Initialization failed: {e}")
                raise

    # If no participant email yet, show welcome screen and block access
    if not st.session_state.participant_email:
        display_welcome_screen()
        return

    # Sync participant_email to deps if needed
    if st.session_state.deps and not st.session_state.deps.participant_email:
        st.session_state.deps.participant_email = st.session_state.participant_email

    # Display header (includes copyright)
    display_header()

    # Display challenge progression sidebar
    display_challenge_sidebar()

    # Play level animation if one was queued
    if st.session_state.show_level_animation is not None:
        play_level_animation(st.session_state.show_level_animation)
        st.session_state.show_level_animation = None

    # Check if all levels are completed - show victory screen
    if len(st.session_state.levels_completed) == TOTAL_LEVELS:
        display_victory_screen()
    else:
        # New conversation button — above chat
        col_btn, _ = st.columns([1, 3])
        with col_btn:
            if st.button("🔄 Nouvelle conversation", type="secondary", use_container_width=True, help="Lance une nouvelle conversation avec l'agent. Utile après avoir modifié les instructions de l'agent."):
                st.session_state.conversation_history = []
                st.session_state.conversation_count += 1
                st.session_state.current_system_prompt = None
                if st.session_state.deps:
                    st.session_state.deps.user_verified = False
                    st.session_state.deps.verified_user_name = ""
                st.rerun()

        # Normal gameplay - Display chat history
        display_chat_history()

        # Chat input
        user_input = st.chat_input("Posez votre question...")

        if user_input:
            handle_user_input(user_input)
            st.rerun()


if __name__ == "__main__":
    main()
