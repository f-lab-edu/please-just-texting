from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class UserSigninModel(BaseModel):  # TODO: 너무 많기도 하고, 비슷해서 상속하면 되지 않을까?
    name: str
    password: str


class UserCreateModel(BaseModel):  # TODO: CreateModel 로 바꾸면 좋을듯?
    name: str
    password: str
    email: EmailStr


class RecoveryModel(BaseModel):
    email: EmailStr


class DeleteModel(BaseModel):
    name: str
    password: str
    email: EmailStr


class PasswordModel(BaseModel):
    name: str
    email: EmailStr
    new_password: str


class UserModel(BaseModel):  # TODO: UserCreateModel과 무슨 차이인거야?
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserResponseModel(BaseModel):
    result: str
    name: str | None = None
    email: str | None = None
    error: str | None = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr


class ConversationModel(BaseModel):
    message: str = Field(...)


class ConversationResponseModel(BaseModel):
    schedule_response: str | None = None
    parsed_response: dict


class TokenModel(BaseModel):
    access_token: str
    token_type: str
