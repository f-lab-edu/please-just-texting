from app.dependencies import session
from app.models.dao.users import check_user_exists
from app.schemas import TokenModel
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestFormStrict
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["token"])


@router.post("/token")
async def singin(
    form_data: OAuth2PasswordRequestFormStrict = Depends(), db: AsyncSession = Depends(session)
) -> TokenModel:
    """
    Authenticate user and Return Token

    - **Args**
        - **form_data (OAuth2PasswordRequestFormStrict)**: form_data instance g containig username, password.
            - **username (str)**: username
            - **password (str)**: password

    - **Returns**
        - **TokenModel**: TokenModel containing "access_token", "token_type"

    - **Raise**
        - **HTTPException**: If user's "name" or "email" is invalid, or any validation error occurs.

    """

    # TODO: 여기에 왜 db가 있죠??? db 는 따로 내부에서만 사용하도록 하고 파라미터로는 받지 말자.
    # TODO: 여기에 DB로부터 입력된 필드값에 해당되는 유저가 있는지 확인하는것이 필요
    # TODO: form_data.username 로 해당되는 유저 가져오고, 해쉬값과 비번값을 비교해서 맞는지 확인
    # TODO: 로직이 추가되면 raise에 Exception 추가해주기

    await check_user_exists(name=form_data.username, db=db)
    return TokenModel(access_token="asdf", token_type="bearer")  # TODO: 임시 access_token 값을 jwt 값으로 수정
