from fastapi import FastAPI
from pydantic_settings import BaseSettings
import uvicorn


app = FastAPI()

class Settings(BaseSettings):
    conf_host: str = "0.0.0.0"
    conf_port: str = "8000"


settings = Settings()


@app.get('/')
def read_root():
    return {'Hello': 'World'}

def run_app() -> None:
    uvicorn.run(app, host=settings.conf_host, port=settings.conf_port)


def main() -> None:
    run_app()


if __name__ == "__main__":
    main()


