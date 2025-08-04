from decimal import Decimal
from http import HTTPStatus
from sqlite3 import IntegrityError
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dataseed import security
from dataseed.application.interfaces.user_repository_interface import (
    UserRepositoryInterface,
)
from dataseed.domain.dto.user_dto import BalanceDTO, UserDTO
from dataseed.models import User as UserModel


class UserRepository(UserRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> Optional[UserModel]:
        user = await self.session.scalar(
            select(UserModel).where(UserModel.email == email)
        )
        return user

    async def create_user(self, user: UserDTO) -> Optional[UserModel]:
        user_db = await self.session.scalar(
            select(UserModel).where(
                (UserModel.username == user.username)
                | (UserModel.email == user.email)
            )
        )

        if user_db:
            field = (
                'Username' if (user_db.username == user.username) else 'Email'
            )
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f'{field} already exists',
            )

        user_db = UserModel(
            username=user.username,
            email=user.email,
            password=security.get_password_hash(user.password),
        )

        self.session.add(user_db)
        await self.session.commit()
        await self.session.refresh(user_db)

        return user_db

    async def list_users(self) -> Optional[list[UserModel]]:
        result = await self.session.scalars(select(UserModel))
        users = result.all()

        return list(users)

    async def update_user(
        self, current_user: UserModel, user: UserDTO
    ) -> UserModel:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = security.get_password_hash(user.password)

        try:
            self.session.add(current_user)
            await self.session.commit()
            await self.session.refresh(current_user)
            return current_user
        except IntegrityError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Resource already exists',
            )

    async def update_balance(
        self, balance: BalanceDTO, user_id: int
    ) -> UserModel:
        user = await self.get_user_by_id(user_id=user_id)

        if balance.food_amount is not None:
            user.food_amount += balance.food_amount

        if balance.meal_amount is not None:
            user.meal_amount += balance.meal_amount

        if balance.cash is not None:
            user.cash += balance.cash

        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Resource already exists',
            )

    async def update_food_amount(
        self, user_id: int, value: Decimal
    ) -> UserModel:
        user = await self.get_user_by_id(user_id=user_id)

        user.food_amount -= value

        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Resource already exists',
            )

    async def update_meal_amount(
        self, user_id: int, value: Decimal
    ) -> UserModel:
        user = await self.get_user_by_id(user_id=user_id)

        user.meal_amount -= value

        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Resource already exists',
            )

    async def update_cash(self, user_id: int, value: Decimal) -> UserModel:
        user = await self.get_user_by_id(user_id=user_id)

        user.cash -= value

        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Resource already exists',
            )

    async def get_user_by_id(self, user_id: int) -> UserModel:
        user = await self.session.scalar(
            select(UserModel).where(UserModel.id == user_id)
        )

        if user is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='User not found',
            )
        return user
