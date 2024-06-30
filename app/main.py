import json

import uvicorn
from app.routers import users
from app.settings import settings
from app.utils import calender_utils
from app.utils import openai_utils
from fastapi import FastAPI
from fastapi import Form
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.include_router(users.router)

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("dialogue_form.html", {"request": request})


@app.post("/submit", response_class=HTMLResponse)
async def submit_dialogue(request: Request, username: str = Form(...), message: str = Form(...)):
    schedule_response: str = openai_utils.getResponseFromOpenai(message)
    parsed_response: dict[str, str] = json.loads(schedule_response)

    if len(set(parsed_response.keys()) & {"title", "date", "description"}) < 3:
        # error 표시용 html로 랜더링.
        raise ValueError(f"{parsed_response=} is not valid.")

    calender_utils.add_event_to_calendar(parsed_response)

    return templates.TemplateResponse(
        "show_response.html",
        {"request": request, "data": parsed_response},
    )


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
