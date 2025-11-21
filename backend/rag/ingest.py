import os
from typing import List
# Placeholder for ChromaDB and Embeddings
# from .store import VectorStore

class IngestionPipeline:
    def __init__(self, watch_dir: str):
        self.watch_dir = watch_dir
        # self.store = VectorStore()
        print(f"Ingestion Pipeline watching: {self.watch_dir}")

    async def process_folder(self, folder_path: str):
        """
        Recursively reads files and ingests them.
        """
        print(f"Ingesting folder: {folder_path}")
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith((".md", ".py", ".js", ".txt")):
                    file_path = os.path.join(root, file)
                    await self._ingest_file(file_path)

    async def _ingest_file(self, file_path: str):
        print(f"Reading file: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # TODO: Use Local LLM to summarize or chunk
            # chunks = self.local_llm.chunk(content)
            # self.store.add(chunks)
            print(f"Ingested {len(content)} bytes from {file_path}")
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
