from pydantic import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    conversations: str = Field(..., env="CONVERSATION")

    class Config:
        env_file = ".env"


settrings = Settings()
