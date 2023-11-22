from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSetting: BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    conversation: str = Field(..., env="CONVERSATION")

    class Config:
        env_file = ".env"


settings = Settings()
