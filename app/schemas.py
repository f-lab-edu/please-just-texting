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


class ConversationModel(BaseModel):
    message: str = Field(...)


class UserResponse(BaseModel):
    result: str
    username: str | None = None
    email: str | None = None
    error: str | None = None


class ConversationResponse(BaseModel):
    schedule_response: str | None = None
    parsed_response: dict
