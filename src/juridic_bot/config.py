"""
Configuração do Bot Jurídico para Concursos
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuração centralizada da aplicação"""

    # Discord
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    DISCORD_APP_ID = os.getenv("DISCORD_APP_ID")
    DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID")
    DISCORD_OWNER_ID = int(os.getenv("DISCORD_OWNER_ID", "0"))

    # OpenRouter
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    # RAG
    TOP_K = int(os.getenv("TOP_K", "5"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1500"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    DOCUMENTS_DIR = BASE_DIR / "knowledge"
    CHROMA_DIR = BASE_DIR / ".chroma"
    LOGS_DIR = BASE_DIR / "logs"

    # System
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")  # Prompt personalizado opcional

    @classmethod
    def validate(cls):
        """Valida configurações essenciais"""
        required = [
            "DISCORD_TOKEN",
            "OPENROUTER_API_KEY",
            "OPENAI_API_KEY"
        ]
        missing = [var for var in required if not getattr(cls, var)]
        if missing:
            raise ValueError(f"Variáveis de ambiente faltando: {', '.join(missing)}")

    @classmethod
    def create_directories(cls):
        """Cria diretórios necessários"""
        cls.DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)