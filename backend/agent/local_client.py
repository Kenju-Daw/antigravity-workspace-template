import aiohttp
import json
import os

class LocalClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = os.getenv("LOCAL_MODEL", "llama3.2") # Default to llama3.2

    async def generate(self, prompt: str) -> str:
        """
        Generates a response from the local Ollama instance.
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("response", "")
                    else:
                        return f"Error: {response.status} - {await response.text()}"
        except Exception as e:
            return f"Local LLM Error: Could not connect to Ollama at {self.base_url}. Is it running?"

    async def embed(self, text: str) -> list[float]:
        """
        Generates embeddings using Ollama.
        """
        url = f"{self.base_url}/api/embeddings"
        payload = {
            "model": self.model,
            "prompt": text
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("embedding", [])
                    else:
                        print(f"Embedding Error: {response.status}")
                        return []
        except Exception as e:
            print(f"Embedding Connection Error: {e}")
            return []
