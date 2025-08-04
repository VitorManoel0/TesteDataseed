from http import HTTPStatus

from fastapi import HTTPException

from dataseed import security
from dataseed.api.schemas.token import Token
from dataseed.application.interfaces.user_repository_interface import (
    UserRepositoryInterface,
)
from dataseed.domain.use_cases.auth_use_case import AuthUseCaseDomain
from dataseed.models import User


class AuthUseCase(AuthUseCaseDomain):
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def authenticate_user(self, email: str, password: str) -> Token:
        user = await self.user_repository.get_user_by_email(email)
        if not user or not security.verify_password(password, user.password):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Incorrect email or password',
            )

        data = {'sub': user.email}
        access_token = security.create_access_token(data)

        return Token(access_token=access_token, token_type='Bearer')

    @staticmethod
    def create_token(user: User) -> Token:
        data = {'sub': user.email}
        access_token = security.create_access_token(data)
        return Token(access_token=access_token, token_type='Bearer')

    @staticmethod
    def refresh_user_token(user: User) -> Token:
        new_access_token = security.create_access_token({'sub': user.email})
        return Token(access_token=new_access_token, token_type='Bearer')
