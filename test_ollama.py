"""
Quick Ollama connectivity test
"""
import requests
import json

print("[TEST] Testing Ollama Connection...")

# Test if Ollama is running
try:
    response = requests.get("http://localhost:11434/api/tags")
    if response.status_code == 200:
        models = response.json()
        print(f"[OK] Ollama is running")
        print(f"Available models: {models}")
    else:
        print(f"[ERROR] Ollama returned status: {response.status_code}")
except Exception as e:
    print(f"[ERROR] Could not connect to Ollama: {e}")
    exit(1)

# Test generating a response
print("\n[TEST] Testing llama3.2 generation...")
try:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": "Say hello in one sentence",
            "stream": False
        }
    )
    if response.status_code == 200:
        result = response.json()
        print(f"[OK] Response: {result.get('response', 'No response')}")
    else:
        print(f"[ERROR] Generation failed: {response.status_code}")
except Exception as e:
    print(f"[ERROR] Generation error: {e}")

print("\n[SUCCESS] Ollama tests complete!")
