from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from dataseed.api.schemas.transaction import (
    TransactionResponseSchema,
    TransactionSchema,
)
from dataseed.application.use_cases.transaction_use_case import (
    TransactionUseCase,
)
from dataseed.database import get_session
from dataseed.infrastructure.db.user_repository import UserRepository

router = APIRouter(prefix='/transaction', tags=['Transaction'])

T_Session = Annotated[AsyncSession, Depends(get_session)]


@router.post('/authorizer', response_model=TransactionResponseSchema)
async def update_user(session: T_Session, transaction: TransactionSchema):
    user_repository = UserRepository(session)
    transaction_use_case = TransactionUseCase(user_repository=user_repository)
    response = await transaction_use_case.process_transaction(
        transaction=transaction
    )
    return response
