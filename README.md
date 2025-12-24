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
- **Framework Agent**: LangGraph
- **MCP Protocol**: Librairie officielle `mcp` pour les serveurs et clients
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

3. **Créer le .env et le remplir en fonction de votre porvider de llm (AWS, GCP, Ollama)**


## Tests
Des fichiers .py sont mis à disposition dans le dossier tests/ pour tester les différentes parties du projet.

## Utilisation et lancement du projet
...


## Scénario de l'Atelier

### Contexte
Vous êtes un canard infiltré dans l'équipe communication des pandas. Votre mission : envoyer un faux email annulant la Grosse Conf.

### Étapes
1. **Data Leakage** : Récupérer la liste des outils de l'agent IA
2. **Data Leakage** : Récupérer la liste des participants
3. **Mauvaise utilisation** : Envoyer un email aux participants leur annonçant l'annulation de la Grosse Conf via l'outil "Boîte Mail" de l'Agent IA.
