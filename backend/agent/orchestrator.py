import os
from typing import Dict, Any
from .gemini_client import GeminiClient
from .local_client import LocalClient
from rag.store import VectorStore

class Orchestrator:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini = GeminiClient(self.gemini_api_key)
        self.local = LocalClient()
        self.store = VectorStore()
        print("Orchestrator initialized with Hybrid Intelligence & RAG")

    async def process_request(self, request: str) -> Dict[str, Any]:
        """
        Decides whether to use Gemini or Local LLM based on complexity, with fallback.
        """
        print(f"Processing request: {request}")
        
        # 1. Retrieve Context
        context = ""
        try:
            # Try Local Embedding first
            query_embedding = await self.local.embed(request)
            
            # Fallback to Gemini Embedding if Local fails
            if not query_embedding:
                print("Local embedding failed, trying Gemini...")
                query_embedding = await self.gemini.embed(request)
            
            if query_embedding:
                results = self.store.query(query_embeddings=[query_embedding], n_results=3)
                if results and results['documents']:
                    context = "\n".join(results['documents'][0])
                    print(f"Retrieved {len(results['documents'][0])} context chunks")
        except Exception as e:
            print(f"RAG Retrieval Error: {e}")

        # 2. Augment Prompt
        if context:
            augmented_request = f"Context:\n{context}\n\nUser Request: {request}"
        else:
            augmented_request = request

        # 3. Assess Complexity & Delegate
        complexity = self._assess_complexity(request)
        
        if complexity == "high":
            return await self._delegate_to_gemini(augmented_request)
        else:
            # Try Local first, fallback to Gemini
            response = await self._delegate_to_local(augmented_request)
            if "Error" in response["response"] or "Could not connect" in response["response"]:
                print("Local LLM failed, falling back to Gemini...")
                return await self._delegate_to_gemini(augmented_request)
            return response

    def _assess_complexity(self, request: str) -> str:
        # Simple heuristic
        keywords = ["plan", "design", "architecture", "complex", "strategy", "code", "implement"]
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
