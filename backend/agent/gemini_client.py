import google.generativeai as genai
import os

class GeminiClient:
    def __init__(self, api_key: str):
        if not api_key:
            print("Warning: GEMINI_API_KEY not set.")
            self.model = None
            return
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    async def generate(self, prompt: str) -> str:
        """
        Generates a response from Gemini.
        """
        if not self.model:
            return "Error: Gemini API Key not configured."
            
        try:
            # Note: generic generate_content is synchronous, but we can wrap it or use async version if available in newer SDKs.
            # For now, keeping it simple. In a real async app, run_in_executor might be needed.
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini Error: {e}"

    async def embed(self, text: str) -> list[float]:
        """
        Generates embeddings using Gemini.
        """
        if not self.model:
            return []
            
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            print(f"Gemini Embedding Error: {e}")
            return []
