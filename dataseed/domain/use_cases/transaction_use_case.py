from abc import ABC, abstractmethod

from dataseed.api.schemas.transaction import TransactionSchema


class TransactionUseCaseDomain(ABC):
    @abstractmethod
    async def process_transaction(self, transaction: TransactionSchema):
        pass
