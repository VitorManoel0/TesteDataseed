from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from dataseed import security
from dataseed.api.schemas.token import Token
from dataseed.application.use_cases.auth_use_case import AuthUseCase
from dataseed.database import get_session
from dataseed.infrastructure.db.user_repository import UserRepository
from dataseed.models import User

router = APIRouter(prefix='/auth', tags=['Authorization'])


T_FormData = Annotated[OAuth2PasswordRequestForm, Depends()]
T_Session = Annotated[AsyncSession, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(security.get_current_user)]


@router.post('/token', response_model=Token)
async def login_for_token(session: T_Session, form_data: T_FormData):
    user_repository = UserRepository(session)
    auth_use_case = AuthUseCase(user_repository)
    token = await auth_use_case.authenticate_user(
        email=form_data.username, password=form_data.password
    )

    return token


@router.post('/refresh_token', response_model=Token)
def refresh_token(session: T_Session, current_user: T_CurrentUser):
    user_repository = UserRepository(session)
    token = AuthUseCase(user_repository).refresh_user_token(user=current_user)

    return token
