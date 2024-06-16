from pydantic import BaseModel
from pydantic import EmailStr


class UserLogin(BaseModel):
    name: str
    password: str


class UserCreate(BaseModel):
    name: str
    password: str
    user_email: EmailStr


class UpdateUser(BaseModel):
    name: str
    password: str
    user_email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    user_email: EmailStr

    class Config:
        from_attributes = True
