from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["default"])


@router.get("/")
async def read_default() -> RedirectResponse:
    return RedirectResponse("/docs")
