from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")

    class Config:
        env_file = ".env"


settings = Settings()
