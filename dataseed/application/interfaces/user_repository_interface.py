from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Optional

from dataseed.domain.dto.user_dto import BalanceDTO, UserDTO
from dataseed.models import User as UserModel


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[UserModel]:
        pass

    @abstractmethod
    async def create_user(self, user: UserDTO) -> Optional[UserModel]:
        pass

    @abstractmethod
    async def list_users(self) -> Optional[list[UserModel]]:
        pass

    @abstractmethod
    async def update_user(
        self, current_user: UserModel, user: UserDTO
    ) -> UserModel:
        pass

    @abstractmethod
    async def update_balance(
        self, balance: BalanceDTO, user_id: int
    ) -> UserModel:
        pass

    @abstractmethod
    async def update_food_amount(
        self, user_id: int, value: Decimal
    ) -> UserModel:
        pass

    @abstractmethod
    async def update_meal_amount(
        self, user_id: int, value: Decimal
    ) -> UserModel:
        pass

    @abstractmethod
    async def update_cash(self, user_id: int, value: Decimal) -> UserModel:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> UserModel:
        pass
