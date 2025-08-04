from decimal import Decimal
from typing import Annotated, Optional

from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr

from utils import sanitize_name


class UserDTO(BaseModel):
    username: Annotated[str, AfterValidator(sanitize_name)]
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)


class BalanceDTO(BaseModel):
    food_amount: Optional[Decimal] | None
    meal_amount: Optional[Decimal] | None
    cash: Optional[Decimal] | None
    model_config = ConfigDict(from_attributes=True)
