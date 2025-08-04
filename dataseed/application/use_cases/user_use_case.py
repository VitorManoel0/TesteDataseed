from decimal import Decimal
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException

from dataseed.api.schemas.user import UserListSchema, UserSchema
from dataseed.domain.dto.user_dto import BalanceDTO, UserDTO
from dataseed.domain.use_cases.user_use_case import UserUseCaseDomain
from dataseed.infrastructure.db.user_repository import UserRepository
from dataseed.models import User as UserModel


class UserUseCase(UserUseCaseDomain):
    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    async def create_user(self, user: UserSchema) -> Optional[UserSchema]:
        user_dto = UserDTO(**user.model_dump())
        user = await self.user_repository.create_user(user_dto)
        return user

    async def list_all_users(self) -> Optional[UserListSchema]:
        users = await self.user_repository.list_users()
        if users is None:
            return UserListSchema(users=[])
        return UserListSchema(users=users)

    async def update_user(
        self, current_user: UserModel, user: UserSchema
    ) -> UserSchema:
        user_dto = UserDTO(**user.model_dump())
        user = await self.user_repository.update_user(
            current_user=current_user, user=user_dto
        )
        return user

    async def update_balance(
        self,
        user_id: int,
        food_amount: Optional[Decimal] = None,
        meal_amount: Optional[Decimal] = None,
        cash: Optional[Decimal] = None,
    ) -> UserSchema:
        values = {
            'food_amount': food_amount,
            'meal_amount': meal_amount,
            'cash': cash,
        }

        negative_values = [
            (name, val)
            for name, val in values.items()
            if val is not None and val < 0
        ]

        if negative_values:
            errors = [f'{name} ({val})' for name, val in negative_values]
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f"Invalid values: {', '.join(errors)}",
            )

        balance_dto = BalanceDTO(
            meal_amount=meal_amount, food_amount=food_amount, cash=cash
        )
        user = await self.user_repository.update_balance(
            user_id=user_id, balance=balance_dto
        )
        return user
