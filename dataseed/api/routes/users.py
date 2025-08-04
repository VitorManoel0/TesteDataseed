from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from dataseed import security
from dataseed.api.schemas.message import MessageSchema
from dataseed.api.schemas.user import (
    UserListSchema,
    UserPublic,
    UserSchema,
)
from dataseed.application.use_cases.user_use_case import UserUseCase
from dataseed.database import get_session
from dataseed.infrastructure.db.user_repository import UserRepository
from dataseed.models import User

router = APIRouter(prefix='/accounts', tags=['Accounts'])

T_Session = Annotated[AsyncSession, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(security.get_current_user)]


@router.post('/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
async def create_account(session: T_Session, user: UserSchema):
    user_repository = UserRepository(session)
    user_use_case = UserUseCase(user_repository=user_repository)
    user = await user_use_case.create_user(user=user)

    return user


@router.get(
    '/get_all', response_model=UserListSchema, status_code=HTTPStatus.OK
)
async def get_all_accounts(session: T_Session):
    user_repository = UserRepository(session)
    user_use_case = UserUseCase(user_repository=user_repository)
    users = await user_use_case.list_all_users()

    return users


@router.put('/{user_id}', response_model=UserPublic)
async def update_user(
    session: T_Session,
    user: UserSchema,
    user_id: int,
    current_user: T_CurrentUser,
):
    verfiy_current_user(current_user.id, user_id)

    user_repository = UserRepository(session)
    user_use_case = UserUseCase(user_repository=user_repository)
    user = await user_use_case.update_user(
        current_user=current_user, user=user
    )
    return user


@router.delete('/{user_id}', response_model=MessageSchema)
async def delete_user(
    user_id: int, session: T_Session, current_user: T_CurrentUser
):
    verfiy_current_user(current_user.id, user_id)

    await session.delete(current_user)
    await session.commit()

    return {'message': 'User successfully removed'}


def verfiy_current_user(current_user_id: int, user_id: int):
    if user_id != current_user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )
