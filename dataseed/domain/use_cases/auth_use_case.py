from abc import abstractmethod
from typing import Optional

from dataseed.api.schemas.token import Token
from dataseed.models import User


class AuthUseCaseDomain:
    @abstractmethod
    async def authenticate_user(
        self, email: str, password: str
    ) -> (Optional)[User]:
        pass

    @staticmethod
    def create_token(user: User) -> Token:
        pass

    @staticmethod
    def refresh_user_token(user: User) -> Token:
        pass
