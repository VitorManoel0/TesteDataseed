from dataseed.api.schemas.transaction import (
    TransactionResponseSchema,
    TransactionSchema,
)
from dataseed.domain.use_cases.transaction_use_case import (
    TransactionUseCaseDomain,
)
from dataseed.infrastructure.db.user_repository import UserRepository


class TransactionUseCase(TransactionUseCaseDomain):
    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    async def process_transaction(self, transaction: TransactionSchema):
        try:
            user_id = int(transaction.account)

            user = await self.user_repository.get_user_by_id(user_id=user_id)

            transaction = self.__map_merchant_to_category(transaction)

            FOOD_MCC_CODES = {'5411', '5412'}
            MEAL_MCC_CODES = {'5811', '5812'}

            # Code FOOD = 5411, 5412
            if transaction.mcc in FOOD_MCC_CODES:
                if user.food_amount < transaction.amount:
                    return TransactionResponseSchema(code='51')

                await self.user_repository.update_food_amount(
                    user_id=user_id, value=transaction.amount
                )

            # Code MEAL = 5811, 5812
            elif transaction.mcc in MEAL_MCC_CODES:
                if user.meal_amount < transaction.amount:
                    return TransactionResponseSchema(code='51')

                await self.user_repository.update_meal_amount(
                    user_id=user_id, value=transaction.amount
                )

            else:
                if user.cash < transaction.amount:
                    return TransactionResponseSchema(code='51')

                await self.user_repository.update_cash(
                    user_id=user_id, value=transaction.amount
                )

            return TransactionResponseSchema(code='00')

        except Exception:
            return TransactionResponseSchema(code='07')

    @staticmethod
    def __map_merchant_to_category(
        transaction: TransactionSchema,
    ) -> TransactionSchema:
        # Transport
        transport_patterns = ['UBER TRIP', 'BILHETEUNICO']
        if transaction.merchant in transport_patterns:
            transaction.mcc = '4111'

        # Meal
        meal_patterns = ['UBER EATS', 'IFOOD', 'RAPPI', 'RESTAURANT']
        if transaction.merchant in meal_patterns:
            transaction.mcc = '5811'

        # Food
        food_patterns = ['SUPERMERCADO', 'MERCADO', 'EXTRA', 'CARREFOUR']
        if transaction.merchant in food_patterns:
            transaction.mcc = '5412'

        return transaction
