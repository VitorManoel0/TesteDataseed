from datetime import datetime
from decimal import Decimal as PyDecimal

from sqlalchemy import func, text
from sqlalchemy.orm import Mapped, mapped_column, registry
from sqlalchemy.types import Numeric
from zoneinfo import ZoneInfo

table_registry = registry()


class BaseModel:
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=datetime.now(tz=ZoneInfo('UTC')),
        nullable=False,
    )


@table_registry.mapped_as_dataclass
class User(BaseModel):
    __tablename__ = 'users'

    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    food_amount: Mapped[PyDecimal] = mapped_column(
        Numeric(10, 2), default=PyDecimal('0.00'), server_default=text('0.00')
    )
    meal_amount: Mapped[PyDecimal] = mapped_column(
        Numeric(10, 2), default=PyDecimal('0.00'), server_default=text('0.00')
    )
    cash: Mapped[PyDecimal] = mapped_column(
        Numeric(10, 2), default=PyDecimal('0.00'), server_default=text('0.00')
    )


@table_registry.mapped_as_dataclass
class Transaction(BaseModel):
    __tablename__ = 'transactions'

    accountId: Mapped[str]
    merchant: Mapped[str]
    mcc: Mapped[str]
    amount: Mapped[PyDecimal] = mapped_column(
        Numeric(10, 2), default=PyDecimal('0.00'), server_default=text('0.00')
    )
