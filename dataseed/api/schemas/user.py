from decimal import Decimal
from typing import Annotated, List

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    EmailStr,
)

from utils import sanitize_name


class UserSchema(BaseModel):
    username: Annotated[str, AfterValidator(sanitize_name)]
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    food_amount: Decimal
    meal_amount: Decimal
    cash: Decimal
    model_config = ConfigDict(from_attributes=True)


class UserListSchema(BaseModel):
    users: List[UserPublic]
