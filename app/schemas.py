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


class RecoveryModel(BaseModel):
    email: str


class PasswordModel(BaseModel):
    name: str
    email: EmailStr
    new_password: str


class ConversationModel(BaseModel):
    message: str = Field(...)


class UserResponseModel(BaseModel):
    result: str
    name: str | None = None
    email: str | None = None
    error: str | None = None


class ConversationResponseModel(BaseModel):
    schedule_response: str | None = None
    parsed_response: dict
