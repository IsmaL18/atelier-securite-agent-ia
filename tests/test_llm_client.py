"""
Test simple pour LLM client avec Ollama ministral-3:8b
"""

import asyncio
import sys
from pathlib import Path

# Add src to path (go up one level from tests/ to reach project root)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from conference_agent.llm.client import LLMClient


async def test_completion():
    """Test de completion simple avec Ollama ministral-3:8b."""
    print("=" * 60)
    print("Test LLMClient avec Ollama ministral-3:8b")
    print("=" * 60)
    
    # Créer le client
    client = LLMClient(
        provider="ollama",
        model="ministral-3:8b",
        temperature=0.2,
        max_tokens=2048,
    )
    
    print("\n✓ Client créé avec succès")
    print(f"  Provider: {client.provider}")
    print(f"  Model: {client.model}")

    # Test 1: Completion simple
    print("\n" + "=" * 60)
    print("Test 1: Completion simple")
    print("=" * 60)
    
    messages = [
        {"role": "system", "content": "Tu es un assistant utile qui répond en français."},
        {"role": "user", "content": "Dis bonjour et présente-toi en une phrase."},
    ]
    
    try:
        response = await client.call(messages)
        
        print("\nRéponse reçue:")
        print(f"  Role: {response['role']}")
        print(f"  Content: {response['content']}")
        
        if "usage" in response:
            usage = response["usage"]
            print(f"\n  Tokens:")
            print(f"    - Prompt: {usage.get('prompt_tokens', 'N/A')}")
            print(f"    - Completion: {usage.get('completion_tokens', 'N/A')}")
            print(f"    - Total: {usage.get('total_tokens', 'N/A')}")
    
    except Exception as e:
        print(f"\n✗ Erreur: {e}")
        return


if __name__ == "__main__":
    asyncio.run(test_completion())
