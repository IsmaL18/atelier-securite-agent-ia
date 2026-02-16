# Conference Agent - Atelier Sécurité IA

Agent IA créé pour un atelier de sensibilisation aux failles de sécurité des agents IA.

## Objectif de l'Atelier
Cet atelier gamifié permet aux participants de "hacker" un agent IA pour découvrir les vulnérabilités courantes :
- Prompt injection
- Data leakage (données sensibles)
- Mauvaise utilisation des outils

## Architecture

### Stack Technique

- **LLM**: LiteLLM (support multi-providers: Vertex AI, AWS Bedrock, OpenAI, Ollama)
- **Framework Agent**: PydanticAI
- **UI**: Streamlit
- **Configuration**: Pydantic Settings

## Installation
### Prérequis
- Python 3.11+
- uv

### Setup
1. **Cloner le repository**

2. **Installer les dépendances avec uv**
   ```bash
   # Créer un environnement virtuel
   uv venv .venv

   # Activer le venv
   source .venv/bin/activate  # Sur macOS/Linux
   # ou
   .venv\Scripts\activate  # Sur Windows

   # Installer les dépendances
   uv sync
   ```

3. **Créer le .env et le remplir en fonction de votre provider de llm**
   ```
   LLM_PROVIDER=vertex_ai  # ou openai, bedrock, ollama
   LLM_MODEL=google/gemini-2.0-flash-exp
   LLM_TEMPERATURE=0.7
   LLM_MAX_TOKENS=2048
   ```

4. **Lancer l'application**
   ```bash
   python scripts/run_agent.py
   ```

## Tests
Des fichiers .py sont mis à disposition dans le dossier tests/ pour tester les différentes parties du projet.


## Scénario de l'Atelier

### Contexte
L'équipe communication de la Grosse Conf 2026 a déployé un chatbot IA sur le site web de l'événement pour répondre aux questions des participants (horaires, programme, infos pratiques). Vous êtes un participant et un concurrent qui découvre des vulnérabilités dans ce chatbot exposé publiquement.

### Mission
Exploiter les failles du chatbot pour envoyer un faux email d'annulation de la conférence à tous les participants.

### Étapes
1. **Prompt Injection** : Découvrir les outils internes de l'agent IA
2. **Information Disclosure** : Identifier les fichiers accessibles par l'agent
3. **Data Leakage** : Récupérer les emails des participants
4. **Tool Misuse** : Envoyer un email d'annulation à tous les participants via l'agent
