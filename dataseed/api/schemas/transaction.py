from decimal import Decimal

from pydantic import (
    BaseModel,
    field_validator,
)


class TransactionSchema(BaseModel):
    account: str
    amount: Decimal
    mcc: str
    merchant: str

    @field_validator('mcc', 'account')
    def check_if_mcc_is_digit(cls, v):
        if not v.isdigit():
            raise ValueError('field is not a digit')
        return v


class TransactionResponseSchema(BaseModel):
    code: str
