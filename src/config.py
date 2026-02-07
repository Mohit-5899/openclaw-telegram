"""
Configuration Management

Uses Pydantic for type-safe configuration with environment variable loading.
"""

from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramSettings(BaseSettings):
    """Telegram bot settings."""
    bot_token: str = Field(..., alias="TELEGRAM_BOT_TOKEN")


class AISettings(BaseSettings):
    """AI/LLM settings."""
    anthropic_api_key: str = Field(..., alias="ANTHROPIC_API_KEY")
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")  # For embeddings
    model: str = Field(default="claude-opus-4-6", alias="AI_MODEL")
    max_tokens: int = Field(default=4096, alias="AI_MAX_TOKENS")


class MemorySettings(BaseSettings):
    """mem0 memory settings."""
    enabled: bool = Field(default=True, alias="MEMORY_ENABLED")
    api_key: Optional[str] = Field(default=None, alias="MEM0_API_KEY")


class RAGSettings(BaseSettings):
    """RAG settings."""
    enabled: bool = Field(default=True, alias="RAG_ENABLED")
    vector_db_path: str = Field(default="./data/vectors", alias="VECTOR_DB_PATH")
    min_score: float = Field(default=0.3, alias="RAG_MIN_SCORE")
    max_results: int = Field(default=10, alias="RAG_MAX_RESULTS")


class MCPSettings(BaseSettings):
    """MCP server settings."""
    github_token: Optional[str] = Field(default=None, alias="GITHUB_PERSONAL_ACCESS_TOKEN")
    notion_token: Optional[str] = Field(default=None, alias="NOTION_API_TOKEN")


class AppSettings(BaseSettings):
    """Application settings."""
    log_level: str = Field(default="info", alias="LOG_LEVEL")
    database_path: str = Field(default="./data/clawdbot.db", alias="DATABASE_PATH")
    max_history_messages: int = Field(default=20, alias="MAX_HISTORY_MESSAGES")


class Config(BaseSettings):
    """Main configuration class that combines all settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # Sub-settings
    telegram: TelegramSettings = Field(default_factory=TelegramSettings)
    ai: AISettings = Field(default_factory=AISettings)
    memory: MemorySettings = Field(default_factory=MemorySettings)
    rag: RAGSettings = Field(default_factory=RAGSettings)
    mcp: MCPSettings = Field(default_factory=MCPSettings)
    app: AppSettings = Field(default_factory=AppSettings)
    
    def __init__(self, **kwargs):
        # Load sub-settings from environment
        super().__init__(
            telegram=TelegramSettings(),
            ai=AISettings(),
            memory=MemorySettings(),
            rag=RAGSettings(),
            mcp=MCPSettings(),
            app=AppSettings(),
            **kwargs
        )
        
        # Ensure data directories exist
        Path(self.app.database_path).parent.mkdir(parents=True, exist_ok=True)
        Path(self.rag.vector_db_path).mkdir(parents=True, exist_ok=True)


# Global config instance
config: Config = None


def load_config() -> Config:
    """Load and return the configuration."""
    global config
    if config is None:
        config = Config()
    return config


def get_config() -> Config:
    """Get the current configuration. Must call load_config() first."""
    if config is None:
        return load_config()
    return config
