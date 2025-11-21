import os
from typing import List
from agent.local_client import LocalClient

class IngestionPipeline:
    def __init__(self, watch_dir: str):
        self.watch_dir = watch_dir
        self.local_llm = LocalClient()
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
            
            # Use Local LLM to summarize
            summary = await self.local_llm.generate(f"Summarize this code/text briefly:\n\n{content[:2000]}")
            print(f"Summary for {os.path.basename(file_path)}: {summary[:100]}...")
            
            # TODO: Store in Vector DB
            # self.store.add(content, summary)
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
