from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class UserSignin(BaseModel):
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


class ConversationModel(BaseModel):
    message: str = Field(...)


class Response(BaseModel):
    result: str
    username: str | None = None
    email: str | None = None
    error: str | None = None
