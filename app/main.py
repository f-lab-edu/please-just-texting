import uvicorn
from app.routers import authentication
from app.routers import conversations
from app.routers import default
from app.routers import users
from app.settings import settings
from fastapi import FastAPI

app = FastAPI()
app.include_router(default.router)
app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(authentication.router)


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
