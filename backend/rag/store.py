import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Any

class VectorStore:
    def __init__(self, persist_directory: str = "backend/data/chroma"):
        try:
            # Create directory if it doesn't exist
            os.makedirs(persist_directory, exist_ok=True)
            
            # Use simpler EphemeralClient for now to avoid rust binding issues
            # You can switch to PersistentClient later once dependencies are stable
            self.client = chromadb.Client()
            self.collection = self.client.get_or_create_collection(name="knowledge_base")
            print(f"VectorStore initialized (in-memory mode)")
        except Exception as e:
            print(f"Warning: VectorStore initialization error: {e}")
            print("Running without persistent storage")
            self.client = None
            self.collection = None

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str], embeddings: List[List[float]] = None):
        """
        Adds documents to the collection. 
        If embeddings are provided, they are used. Otherwise, Chroma's default is used (if configured).
        Since we want to use our LocalClient for embeddings, we should pass them in.
        """
        if not self.collection:
            print("VectorStore not initialized, skipping document add")
            return
            
        if embeddings:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids,
                embeddings=embeddings
            )
        else:
            # Fallback to default if no embeddings provided (not recommended if we want specific local model)
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
        print(f"Added {len(documents)} documents to VectorStore.")

    def query(self, query_embeddings: List[List[float]], n_results: int = 5) -> Dict[str, Any]:
        """
        Queries the collection using embeddings.
        """
        if not self.collection:
            return {"documents": [], "metadatas": [], "ids": []}
            
        results = self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results
        )
        return results
