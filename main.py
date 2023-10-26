import uvicorn
from fastapi import FastAPI
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

app = FastAPI()


class Settings(BaseSettings):
    conf_debug: bool = True
    conf_host: str = "0.0.0.0"
    conf_port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()


@app.get("/")
def read_root():
    return {"Hello": "World5"}


def run_app() -> None:
    uvicorn.run(
        "main:app",
        host=settings.conf_host,
        port=settings.conf_port,
        reload=settings.conf_debug,
    )


def main() -> None:
    run_app()


if __name__ == "__main__":
    main()
