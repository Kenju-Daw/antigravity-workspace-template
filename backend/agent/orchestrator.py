import os
from typing import Dict, Any
from .gemini_client import GeminiClient
from .local_client import LocalClient

class Orchestrator:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini = GeminiClient(self.gemini_api_key)
        self.local = LocalClient()
        print("Orchestrator initialized with Hybrid Intelligence")

    async def process_request(self, request: str) -> Dict[str, Any]:
        """
        Decides whether to use Gemini or Local LLM based on complexity.
        """
        print(f"Processing request: {request}")
        
        complexity = self._assess_complexity(request)
        
        if complexity == "high":
            return await self._delegate_to_gemini(request)
        else:
            return await self._delegate_to_local(request)

    def _assess_complexity(self, request: str) -> str:
        # Simple heuristic
        keywords = ["plan", "design", "architecture", "complex", "strategy"]
        if any(k in request.lower() for k in keywords):
            return "high"
        return "low"

    async def _delegate_to_gemini(self, request: str):
        print("Delegating to Gemini (Manager)...")
        response = await self.gemini.generate(request)
        return {"source": "Gemini", "response": response}

    async def _delegate_to_local(self, request: str):
        print("Delegating to Local LLM (Worker)...")
        response = await self.local.generate(request)
        return {"source": "Local", "response": response}
