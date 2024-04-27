from app.dependencies import get_db
from app.models.base import User
from app.models.dao.users import create_user
from app.models.dao.users import delete_user
from app.models.dao.users import get_user
from app.models.dao.users import get_users
from app.models.dao.users import update_user
from app.schemas import UpdateUser
from app.schemas import UserCreate
from app.schemas import UserResponse
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/users/", response_model=UserResponse)
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)) -> User:
    return await create_user(user=user, db=db)


@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user_endpoint(user_id: int, db: Session = Depends(get_db)) -> User:
    return await get_user(user_id=user_id, db=db)


@router.get("/users/", response_model=list[UserResponse])
async def read_users_endpoint(db: Session = Depends(get_db)) -> list[User]:
    return await get_users(db=db)


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user_endpoint(
    user_id: int, user: UpdateUser, db: Session = Depends(get_db)
) -> User:
    return await update_user(db=db, user_id=user_id, user=user)


@router.delete("/users/{user_id}", status_code=204)
async def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)) -> dict:
    await delete_user(db=db, user_id=user_id)
