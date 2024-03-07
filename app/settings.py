from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    conversation: str = Field(..., env="CONVERSATION")

    class Config:
        env_file = ".env"


settings = Settings()
