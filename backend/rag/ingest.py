import os
import uuid
from typing import List
from agent.local_client import LocalClient
from .store import VectorStore

class IngestionPipeline:
    def __init__(self, watch_dir: str):
        self.watch_dir = watch_dir
        self.local_llm = LocalClient()
        self.store = VectorStore()
        print(f"Ingestion Pipeline watching: {self.watch_dir}")

    async def process_folder(self, folder_path: str):
        """
        Recursively reads files and ingests them.
        """
        print(f"Ingesting folder: {folder_path}")
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith((".md", ".py", ".js", ".txt", ".html", ".css", ".json")):
                    file_path = os.path.join(root, file)
                    await self._ingest_file(file_path)

    async def _ingest_file(self, file_path: str):
        print(f"Reading file: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if not content.strip():
                return

            # Generate embedding
            embedding = await self.local_llm.embed(content)
            if not embedding:
                print(f"Failed to generate embedding for {file_path}")
                return

            # Generate summary (optional, but good for RAG context)
            # summary = await self.local_llm.generate(f"Summarize: {content[:1000]}")

            # Store in Vector DB
            self.store.add_documents(
                documents=[content],
                metadatas=[{"source": file_path, "filename": os.path.basename(file_path)}],
                ids=[str(uuid.uuid4())],
                embeddings=[embedding]
            )
            print(f"Ingested {os.path.basename(file_path)}")
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
