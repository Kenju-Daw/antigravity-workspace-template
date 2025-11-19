import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings managed by Pydantic."""
    
    # Google GenAI Configuration
    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL_NAME: str = "gemini-2.0-flash-exp" # Default to latest
    
    # Agent Configuration
    AGENT_NAME: str = "AntigravityAgent"
    DEBUG_MODE: bool = False
    
    # Memory Configuration
    MEMORY_FILE: str = "agent_memory.json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Global settings instance
settings = Settings()
