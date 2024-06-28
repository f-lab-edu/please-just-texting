from app.dependencies import get_db
from app.models.base import User
from app.models.dao.users import check_user_exists
from app.models.dao.users import create_user
from app.models.dao.users import delete_user
from app.models.dao.users import get_db_user
from app.models.dao.users import update_user
from app.schemas import Response
from app.schemas import UpdateUser
from app.schemas import UserCreate
from app.schemas import UserSignin
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["users"], default_response_class=JSONResponse)

templates = Jinja2Templates(directory="app/templates")


@router.post("/signin", summary="Signin")
async def signin(
    username: str,
    password: str,
    db: AsyncSession = Depends(get_db),
) -> Response:
    """
    Authenticate a user

    - **username (str)**: username to signin
    - **password (str)**: password to signin
    """

    user = UserSignin(name=username, password=password)
    try:
        await check_user_exists(db, user)
    except HTTPException as e:
        return Response(result="fail", error=e)
    return Response(result="success")


@router.post("/signup", summary="signup")
async def create_user_endpoint(
    username: str,
    password: str,
    email: str,
    db: AsyncSession = Depends(get_db),
) -> Response:
    """
    Create user

    - **username (str)**: username
    - **password (str)**: password
    - **email (str)** : user email(used for recovery)
    """

    try:
        user = UserCreate(name=username, password=password, user_email=email)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    db_user = await create_user(user=user, db=db)
    return Response(result="success", username=db_user.name, email=db_user.email)


@router.post("/recovery", summary="recover account")
async def read_find_account_response_form(
    email: str, db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Find Username by email

    - **email (str)**: email associated with username
    """

    user: User | None = await get_db_user(field=email, db=db)
    if user:
        return {"result": "success", "username": user.name}
    raise HTTPException(status_code=404, detail="Username not found")


@router.post("/password", response_class=HTMLResponse)
async def read_password_response_form(
    request: Request,
    username: str,
    email: str,
    new_password: str,
    db: AsyncSession = Depends(get_db),
):
    user = UpdateUser(name=username, password=new_password, user_email=email)
    await update_user(user=user, db=db)
    return templates.TemplateResponse(
        "reset_password_response_form.html", {"request": request}
    )


@router.delete("/users/{user_id}", status_code=204)
async def delete_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    await delete_user(db=db, user_id=user_id)
