import json

from app.schemas import ConversationModel
from app.schemas import ConversationResponse
from app.utils import calender_utils
from app.utils import openai_utils
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(default_response_class=JSONResponse, tags=["conversation"])


@router.post("/conversation")
async def submit_dialogue(conversation: ConversationModel) -> ConversationResponse:
    """
    Create event to calendar with all information:

    - **message**: conversation containing date.
    """

    schedule_response: str = openai_utils.getResponseFromOpenai(conversation.message)
    parsed_response: dict[str, str] = json.loads(schedule_response)
    calender_utils.add_event_to_calendar(parsed_response)

    return ConversationResponse(
        schedule_response=schedule_response, parsed_response=parsed_response
    )
