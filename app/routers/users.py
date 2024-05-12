from app.dependencies import get_db
from app.models.dao.users import check_user_exists
from app.models.dao.users import create_user
from app.models.dao.users import delete_user
from app.models.dao.users import get_user
from app.models.dao.users import update_user
from app.schemas import UpdateUser
from app.schemas import UserCreate
from app.schemas import UserLogin
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
async def read_login_form(request: Request):
    return templates.TemplateResponse("login_form.html", {"request": request})


@router.post("/login/submit", response_class=HTMLResponse)
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    user = UserLogin(name=username, password=password)
    await check_user_exists(db, user)
    return templates.TemplateResponse("dialogue_form.html", {"request": request})


@router.get("/create_account", response_class=HTMLResponse)
async def read_create_account_form(request: Request):
    return templates.TemplateResponse("create_account_form.html", {"request": request})


@router.post("/create_account/submit", response_class=HTMLResponse)
async def create_user_endpoint(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    user = UserCreate(name=username, password=password, user_email=email)
    db_user = await create_user(user=user, db=db)
    return templates.TemplateResponse(
        "create_account_response_form.html", {"request": request, "data": db_user}
    )


@router.get("/find_account", response_class=HTMLResponse)
async def read_find_account_form(request: Request):
    return templates.TemplateResponse("find_account_form.html", {"request": request})


@router.post("/find_account/submit", response_class=HTMLResponse)
async def read_find_account_response_form(
    request: Request, email: str = Form(...), db: AsyncSession = Depends(get_db)
):
    db_user = await get_user(email=email, db=db)
    return templates.TemplateResponse(
        "find_account_response_form.html", {"request": request, "data": db_user}
    )


@router.get("/reset_password", response_class=HTMLResponse)
async def read_password_form(request: Request):
    return templates.TemplateResponse("reset_password_form.html", {"request": request})


@router.post("/reset_password/submit", response_class=HTMLResponse)
async def read_password_response_form(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    new_password: str = Form(...),
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
