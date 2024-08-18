import json

from app.dependencies import oauth2_scheme
from app.schemas import ConversationModel
from app.schemas import ConversationResponseModel
from app.utils import calender_utils
from app.utils import openai_utils
from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse

router = APIRouter(default_response_class=JSONResponse, tags=["conversation"])


@router.post("/conversation")
async def submit_dialogue(
    conversation: ConversationModel, token: str = Depends(oauth2_scheme)
) -> ConversationResponseModel:
    """
    Create event to calendar with all information:

    - **Args**:
        - **conversation (ConversationModel)**: An object containing "message".
        - **message (str)**: conversation containing date.

    - **Returns**:
        - **ConversationalResponseModel**: A reponse model containig "schedule_response", "parsed_response".
            - **schedule_response (str)**: response containig schedule info.
            - **parsed_response (dict)**: serialized schedule_response.
    - **Raise**
        - **HTTPException**: If user's convesation is invalid, or any validation error occurs.

    """

    schedule_response: str = openai_utils.getResponseFromOpenai(conversation.message)
    parsed_response: dict[str, str] = json.loads(schedule_response)
    calender_utils.add_event_to_calendar(parsed_response)

    return ConversationResponseModel(schedule_response=schedule_response, parsed_response=parsed_response)
