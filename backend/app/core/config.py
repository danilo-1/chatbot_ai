from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Ajusta o caminho para o diretório raiz do backend
openai_api_key_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(openai_api_key_path)

class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY", description="OpenAI API Key")
    allowed_origin: str = Field(default="http://localhost:5173", env="ALLOWED_ORIGIN")

    class Config:
        env_file = str(openai_api_key_path)
        env_file_encoding = "utf-8"
        case_sensitive = False
        frozen = True  # Torna a instância imutável e hashable

@lru_cache
def get_settings() -> Settings:
    return Settings()