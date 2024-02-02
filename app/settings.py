from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    conf_debug: bool = True
    conf_host: str = "0.0.0.0"
    conf_port: int = 8000
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")

    user_name: str = Field(..., env="USER_NAME")
    user_password: str = Field(..., env="USER_PASSWORD")

    class Config:
        env_file = ".env"


settings = Settings()
