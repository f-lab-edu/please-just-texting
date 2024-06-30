from app.dependencies import get_db
from app.models.base import User
from app.models.dao.users import check_user_exists
from app.models.dao.users import create_user
from app.models.dao.users import delete_user
from app.models.dao.users import get_user_by_email
from app.models.dao.users import update_user
from app.schemas import DeleteModel
from app.schemas import PasswordModel
from app.schemas import RecoveryModel
from app.schemas import UserCreateModel
from app.schemas import UserModel
from app.schemas import UserResponseModel
from app.schemas import UserSigninModel
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["users"], default_response_class=JSONResponse)


@router.post("/signin", summary="Signin")
async def signin(
    user: UserSigninModel,
    db: AsyncSession = Depends(get_db),
) -> UserResponseModel:
    """
    Authenticate a user

    - **username (str)**: username to signin
    - **password (str)**: password to signin
    """

    try:
        await check_user_exists(db, user)
    except HTTPException as e:
        return UserResponseModel(result="fail", error=e.detail)
    return UserResponseModel(result="success")


@router.post("/signup", summary="signup")
async def create_user_endpoint(
    user: UserCreateModel,
    db: AsyncSession = Depends(get_db),
) -> UserResponseModel:
    """
    Create user

    - **username (str)**: username
    - **password (str)**: password
    - **email (str)** : user email(used for recovery)
    """

    user: UserModel = await create_user(user=user, db=db)
    return UserResponseModel(result="success", name=user.name, email=user.email)


@router.post("/recovery", summary="recover account")
async def read_find_account_response_form(
    user: RecoveryModel,
    db: AsyncSession = Depends(get_db),
) -> UserResponseModel:
    """
    Find Username by email

    - **email (str)**: email associated with username
    """

    user: User = await get_user_by_email(email=user.email, db=db)
    if user:
        return UserResponseModel(result="success", name=user.name)
    raise HTTPException(status_code=404, detail="Username not found")


@router.post("/password", summary="reset password")
async def read_password_response_form(
    user: PasswordModel,
    db: AsyncSession = Depends(get_db),
) -> UserResponseModel:
    """
    Reset Password by new_password

    - **name (str)**: username
    - **email (EmailStr)**: password
    - **new_password (str)**: new password
    """

    await update_user(user=user, db=db)
    return UserResponseModel(result="sucess")


@router.delete("/delete", summary="delete user")
async def delete_user_endpoint(
    user: DeleteModel,
    db: AsyncSession = Depends(get_db),
) -> UserResponseModel:
    """
    Detele user by name, password, email

    - **name (str)**: username
    - **password (str)**: password
    - **email (Emailstr)**: email
    """

    await delete_user(user=user, db=db)
    return UserResponseModel(result="success")
