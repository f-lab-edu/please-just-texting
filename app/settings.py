from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    conf_debug: bool = True
    conf_host: str = "0.0.0.0"
    conf_port: int = 8000

    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    imporsonation_account: str = Field(..., env="IMPERSONATION_ACCOUNT")

    database_host: str
    database_port: int
    database_username: str
    database_password: str
    database_name: str

    class Config:
        env_file = ".env"
        env_prefix = "CONF_"


settings = Settings()
