from decimal import Decimal
from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from dataseed.api.schemas.user import UserPublic
from dataseed.application.use_cases.user_use_case import UserUseCase
from dataseed.database import get_session
from dataseed.infrastructure.db.user_repository import UserRepository

router = APIRouter(prefix='/management', tags=['Management'])

T_Session = Annotated[AsyncSession, Depends(get_session)]


@router.put('/add_balance_in_account/{user_id}', response_model=UserPublic)
async def update_user(
    session: T_Session,
    user_id: int,
    food_amount: Decimal = None,
    meal_amount: Decimal = None,
    cash: Decimal = None,
):
    user_repository = UserRepository(session)
    user_use_case = UserUseCase(user_repository=user_repository)
    user = await user_use_case.update_balance(
        user_id=user_id,
        food_amount=food_amount,
        meal_amount=meal_amount,
        cash=cash,
    )
    return user
