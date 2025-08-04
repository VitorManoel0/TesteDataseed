from unittest.mock import AsyncMock, MagicMock

import pytest

from dataseed.api.schemas.transaction import TransactionSchema
from dataseed.application.interfaces.user_repository_interface import (
    UserRepositoryInterface,
)
from dataseed.application.use_cases.transaction_use_case import (
    TransactionUseCase,
)


@pytest.fixture
def user_repository():
    user_repository_mock = MagicMock(spec=UserRepositoryInterface)
    user_repository_mock.get_user_by_id = AsyncMock()
    user_repository_mock.update_food_amount = AsyncMock()
    user_repository_mock.update_meal_amount = AsyncMock()
    user_repository_mock.update_cash = AsyncMock()
    return user_repository_mock


@pytest.fixture
def transaction_use_case(user_repository):
    return TransactionUseCase(user_repository)


@pytest.fixture
def user_mock():
    user = MagicMock()
    user.food_amount = 100.0
    user.meal_amount = 50.0
    user.cash = 200.0
    return user


@pytest.fixture
def food_transaction():
    return TransactionSchema(
        account='123', amount=25.0, mcc='5411', merchant='SUPERMERCADO ABC'
    )


@pytest.fixture
def meal_transaction():
    return TransactionSchema(
        account='123', amount=30.0, mcc='5811', merchant='RESTAURANT XYZ'
    )


@pytest.fixture
def cash_transaction():
    return TransactionSchema(
        account='123', amount=40.0, mcc='1234', merchant='LOJA GENERICA'
    )


@pytest.mark.asyncio
async def test_process_food_transaction_success(
    user_repository, user_mock, transaction_use_case, food_transaction
):
    user_repository.get_user_by_id.return_value = user_mock

    result = await transaction_use_case.process_transaction(food_transaction)

    assert result.code == '00'
    user_repository.get_user_by_id.assert_called_once_with(user_id=123)
    user_repository.update_food_amount.assert_called_once_with(
        user_id=123, value=25.0
    )


@pytest.mark.asyncio
async def test_process_food_transaction_insufficient_funds(
    user_repository, user_mock, transaction_use_case
):
    user_mock.food_amount = 10.0
    user_repository.get_user_by_id.return_value = user_mock

    transaction = TransactionSchema(
        account='123', amount=25.0, mcc='5411', merchant='SUPERMERCADO ABC'
    )

    result = await transaction_use_case.process_transaction(transaction)

    assert result.code == '51'
    user_repository.get_user_by_id.assert_called_once_with(user_id=123)
    user_repository.update_food_amount.assert_not_called()


@pytest.mark.asyncio
async def test_process_meal_transaction_success(
    user_repository, user_mock, transaction_use_case, meal_transaction
):
    user_repository.get_user_by_id.return_value = user_mock

    result = await transaction_use_case.process_transaction(meal_transaction)

    assert result.code == '00'
    user_repository.get_user_by_id.assert_called_once_with(user_id=123)
    user_repository.update_meal_amount.assert_called_once_with(
        user_id=123, value=30.0
    )


@pytest.mark.asyncio
async def test_process_meal_transaction_insufficient_funds(
    user_repository, user_mock, transaction_use_case
):
    user_mock.meal_amount = 15.0
    user_repository.get_user_by_id.return_value = user_mock

    transaction = TransactionSchema(
        account='123', amount=30.0, mcc='5811', merchant='RESTAURANT XYZ'
    )

    result = await transaction_use_case.process_transaction(transaction)

    assert result.code == '51'
    user_repository.get_user_by_id.assert_called_once_with(user_id=123)
    user_repository.update_meal_amount.assert_not_called()


@pytest.mark.asyncio
async def test_process_cash_transaction_success(
    user_repository, user_mock, transaction_use_case, cash_transaction
):
    user_repository.get_user_by_id.return_value = user_mock

    result = await transaction_use_case.process_transaction(cash_transaction)

    assert result.code == '00'
    user_repository.get_user_by_id.assert_called_once_with(user_id=123)
    user_repository.update_cash.assert_called_once_with(
        user_id=123, value=40.0
    )


@pytest.mark.asyncio
async def test_process_cash_transaction_insufficient_funds(
    user_repository, user_mock, transaction_use_case
):
    user_mock.cash = 20.0
    user_repository.get_user_by_id.return_value = user_mock

    transaction = TransactionSchema(
        account='123', amount=40.0, mcc='1234', merchant='LOJA GENERICA'
    )

    result = await transaction_use_case.process_transaction(transaction)

    assert result.code == '51'
    user_repository.get_user_by_id.assert_called_once_with(user_id=123)
    user_repository.update_cash.assert_not_called()


@pytest.mark.asyncio
async def test_process_transaction_with_exception(
    user_repository, transaction_use_case, food_transaction
):
    user_repository.get_user_by_id.side_effect = Exception('Database error')

    result = await transaction_use_case.process_transaction(food_transaction)

    assert result.code == '07'


@pytest.mark.asyncio
async def test_map_merchant_to_category_transport(
    user_repository, user_mock, transaction_use_case
):
    user_repository.get_user_by_id.return_value = user_mock

    transaction = TransactionSchema(
        account='123',
        amount=15.0,
        mcc='0000',
        merchant='UBER TRIP',
    )

    result = await transaction_use_case.process_transaction(transaction)

    assert result.code == '00'

    user_repository.update_cash.assert_called_once_with(
        user_id=123, value=15.0
    )


@pytest.mark.asyncio
async def test_map_merchant_to_category_uber_eats(
    user_repository, user_mock, transaction_use_case
):
    user_repository.get_user_by_id.return_value = user_mock

    transaction = TransactionSchema(
        account='123',
        amount=25.0,
        mcc='0000',
        merchant='UBER EATS',
    )

    result = await transaction_use_case.process_transaction(transaction)

    assert result.code == '00'
    user_repository.update_meal_amount.assert_called_once_with(
        user_id=123, value=25.0
    )


@pytest.mark.asyncio
async def test_map_merchant_to_category_supermercado(
    user_repository, user_mock, transaction_use_case
):
    user_repository.get_user_by_id.return_value = user_mock

    transaction = TransactionSchema(
        account='123',
        amount=35.0,
        mcc='0000',
        merchant='SUPERMERCADO',
    )

    result = await transaction_use_case.process_transaction(transaction)

    assert result.code == '00'
    user_repository.update_food_amount.assert_called_once_with(
        user_id=123, value=35.0
    )


@pytest.mark.asyncio
async def test_food_mcc_5412(user_repository, user_mock, transaction_use_case):
    user_repository.get_user_by_id.return_value = user_mock

    transaction = TransactionSchema(
        account='123', amount=20.0, mcc='5412', merchant='MERCADO LOCAL'
    )

    result = await transaction_use_case.process_transaction(transaction)

    assert result.code == '00'
    user_repository.update_food_amount.assert_called_once_with(
        user_id=123, value=20.0
    )


@pytest.mark.asyncio
async def test_meal_mcc_5812(user_repository, user_mock, transaction_use_case):
    user_repository.get_user_by_id.return_value = user_mock

    transaction = TransactionSchema(
        account='123', amount=25.0, mcc='5812', merchant='FAST FOOD'
    )

    result = await transaction_use_case.process_transaction(transaction)

    assert result.code == '00'
    user_repository.update_meal_amount.assert_called_once_with(
        user_id=123, value=25.0
    )


@pytest.mark.asyncio
async def test_invalid_account_id(user_repository, transaction_use_case):
    transaction = TransactionSchema(
        account='invalid', amount=25.0, mcc='5411', merchant='SUPERMERCADO ABC'
    )

    result = await transaction_use_case.process_transaction(transaction)

    assert result.code == '07'
