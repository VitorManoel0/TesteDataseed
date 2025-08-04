from decimal import Decimal

from pydantic import (
    BaseModel,
)


class TransactionSchema(BaseModel):
    account: str
    amount: Decimal
    mcc: str
    merchant: str


class TransactionResponseSchema(BaseModel):
    code: str
