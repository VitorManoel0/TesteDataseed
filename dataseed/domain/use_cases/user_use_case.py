from abc import abstractmethod
from decimal import Decimal
from typing import Optional

from dataseed.api.schemas.user import UserListSchema, UserSchema
from dataseed.models import User as UserModel


class UserUseCaseDomain:
    @abstractmethod
    async def create_user(self, user: UserSchema) -> Optional[UserModel]:
        pass

    @abstractmethod
    async def list_all_users(self) -> Optional[UserListSchema]:
        pass

    @abstractmethod
    async def update_user(
        self, current_user: UserModel, user: UserSchema
    ) -> UserSchema:
        pass

    @abstractmethod
    async def update_balance(
        self,
        user_id: int,
        food_amount: Optional[Decimal] = None,
        meal_amount: Optional[Decimal] = None,
        cash: Optional[Decimal] = None,
    ) -> UserSchema:
        pass
