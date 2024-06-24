import json

from app.utils import calender_utils
from app.utils import openai_utils
from fastapi import APIRouter
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(default_response_class=HTMLResponse, tags=["conversation"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/conversation")
async def read_form():
    return templates.TemplateResponse(name="dialogue_form.html")


@router.post("/conversation")
async def submit_dialogue(message: str = Form(...)):
    schedule_response: str = openai_utils.getResponseFromOpenai(message)
    parsed_response: dict[str, str] = json.loads(schedule_response)
    calender_utils.add_event_to_calendar(parsed_response)

    return templates.TemplateResponse(
        name="show_response.html", context={"data": parsed_response}
    )
