import json
import os
from typing import List, Dict, Any
from src.config import settings

class MemoryManager:
    """Simple JSON-file based memory manager for the agent."""

    def __init__(self, memory_file: str = settings.MEMORY_FILE):
        self.memory_file = memory_file
        self._memory: List[Dict[str, Any]] = []
        self._load_memory()

    def _load_memory(self):
        """Loads memory from the JSON file if it exists."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self._memory = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode memory file {self.memory_file}. Starting fresh.")
                self._memory = []
        else:
            self._memory = []

    def save_memory(self):
        """Saves the current memory state to the JSON file."""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self._memory, f, indent=2, ensure_ascii=False)

    def add_entry(self, role: str, content: str, metadata: Dict[str, Any] = None):
        """Adds a new interaction to memory."""
        entry = {
            "role": role,
            "content": content,
            "metadata": metadata or {}
        }
        self._memory.append(entry)
        self.save_memory()

    def get_history(self) -> List[Dict[str, Any]]:
        """Returns the full conversation history."""
        return self._memory

    def clear_memory(self):
        """Clears the agent's memory."""
        self._memory = []
        self.save_memory()
