from app.dependencies import get_db
from app.dependencies import oauth2_scheme
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
    user: UserSigninModel, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> UserResponseModel:
    """
    Authenticate a user

    - **Args**
        - **user (UserSigninModel)**: An object containing user's "name", "password".
            - **name (str)**: username
            - **password (str)**: password
        - **db (AsyncSession)**: The database session dependency.

    - **Returns**
        - **UserResponseModel**: A response model containing "result", "name", "email", "error" message.

    - **Raise**
        - **HTTPException**: If user's "name" or "email" is invalid, or any validation error occurs.
    """

    try:
        await check_user_exists(db, user)
    except HTTPException as e:
        return UserResponseModel(result="fail", error=e.detail)
    return UserResponseModel(result="success")


@router.post("/signup", summary="signup")
async def signup(
    user: UserCreateModel,
    db: AsyncSession = Depends(get_db),
) -> UserResponseModel:
    """
    Create user

    - **Args**
        - **user (UserCreateModel)**: An object containing user's "name", "password", "email".
            - **name (str)**: username
            - **password (str)**: password
            - **email (EmailStr)**: email
        - **db (AsyncSession)**: The database session dependency.

    - **Returns**
        - **UserResponseModel**: A response model containing "result", "name", "email", "error" message.

    - **Raise**
        - **HTTPException**: If user's "name" or "email" is invalid, or any validation error occurs.
    """

    user: UserModel = await create_user(user=user, db=db)
    return UserResponseModel(result="success", name=user.name, email=user.email)


@router.post("/recovery", summary="recover account")
async def recovery_name(
    user: RecoveryModel,
    db: AsyncSession = Depends(get_db),
) -> UserResponseModel:
    """
    Find "name" by "email"

    - **Args**
        - **user (RecoveryModel)**: An object containing user's "email".
            - **email (EmailStr)**: email
        - **db (AsyncSession)**: The database session dependency.

    - **Returns**
        - **UserResponseModel**: A response model containing "result", "name", "email", "error" message.

    - **Raise**
        - **HTTPException**: If user's "name" or "email" is invalid, or any validation error occurs.

    """

    user: User = await get_user_by_email(email=user.email, db=db)
    if user:
        return UserResponseModel(result="success", name=user.name)
    raise HTTPException(status_code=404, detail="Username not found")


@router.post("/password", summary="reset password")
async def reset_password(
    user: PasswordModel,
    db: AsyncSession = Depends(get_db),
) -> UserResponseModel:
    """
    Reset Password by new_password

    - **Args**
        - **user (PasswordModel)**: An object containing user's "name", "email", "new_password".
            - **name (str)**: username
            - **email (EmailStr)**: email
            - **new_password (str)**: new password
        - **db (AsyncSession)**: The database session dependency.

    - **Returns**
        - **UserResponseModel**: A response model containing "result", "name", "email", "error" message.

    - **Raise**
        - **HTTPException**: If user's "name" or "email" is invalid, or any validation error occurs.
    """

    await update_user(user=user, db=db)
    return UserResponseModel(result="sucess")


@router.delete("/delete", summary="delete user")
async def delete(
    user: DeleteModel,
    db: AsyncSession = Depends(get_db),
) -> UserResponseModel:
    """
    Detele user by "name", "password", "email"

    - **Arg**
        - **user (DeleteModel)**: An object containing user's "name", "password", "email".
            - **name (str)**: username
            - **password (str)**: password
            - **email (Emailstr)**: email

    - **Return**
        - **UserResponseModel**: A response model containing "result", "name", "email", "error" message.

    - **Raise**
        - **HTTPException**: If user's "name" or "email" is invalid, or any validation error occurs.
    """

    await delete_user(user=user, db=db)
    return UserResponseModel(result="success")
