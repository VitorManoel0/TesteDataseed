from decimal import Decimal
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from dataseed.api.schemas.user import UserListSchema, UserPublic, UserSchema
from dataseed.application.interfaces.user_repository_interface import (
    UserRepositoryInterface,
)
from dataseed.application.use_cases.user_use_case import UserUseCase
from dataseed.domain.dto.user_dto import BalanceDTO, UserDTO
from dataseed.models import User as UserModel


@pytest.fixture
def user_repository():
    user_repository_mock = MagicMock(spec=UserRepositoryInterface)
    user_repository_mock.create_user = AsyncMock()
    user_repository_mock.list_users = AsyncMock()
    user_repository_mock.update_user = AsyncMock()
    user_repository_mock.update_balance = AsyncMock()
    return user_repository_mock


@pytest.fixture
def user_use_case(user_repository):
    return UserUseCase(user_repository)


@pytest.fixture
def user_schema():
    return UserSchema(
        username='joaosilva', email='joao@example.com', password='password123'
    )


@pytest.fixture
def user_model():
    user = MagicMock(spec=UserModel)
    user.id = 1
    user.username = 'joaosilva'
    user.email = 'joao@example.com'
    user.food_amount = Decimal('100.00')
    user.meal_amount = Decimal('50.00')
    user.cash = Decimal('200.00')
    return user


@pytest.fixture
def user_dto():
    return UserDTO(
        username='joaosilva', email='joao@example.com', password='password123'
    )


@pytest.mark.asyncio
async def test_create_user_success(
    user_repository, user_use_case, user_schema, user_dto
):
    expected_user = user_schema
    user_repository.create_user.return_value = expected_user

    result = await user_use_case.create_user(user_schema)

    assert result == expected_user
    user_repository.create_user.assert_called_once()

    call_args = user_repository.create_user.call_args[0][0]
    assert isinstance(call_args, UserDTO)
    assert call_args.username == user_schema.username
    assert call_args.email == user_schema.email


@pytest.mark.asyncio
async def test_create_user_returns_none(
    user_repository, user_use_case, user_schema
):
    user_repository.create_user.return_value = None

    result = await user_use_case.create_user(user_schema)

    assert result is None
    user_repository.create_user.assert_called_once()


@pytest.mark.asyncio
async def test_list_all_users_success(user_repository, user_use_case):
    mock_users = [
        UserPublic(
            id=1,
            username='user1',
            email='user1@example.com',
            food_amount=Decimal('10.00'),
            meal_amount=Decimal('50.00'),
            cash=Decimal('100.00'),
        ),
        UserPublic(
            id=2,
            username='user2',
            email='user2@example.com',
            food_amount=Decimal('10.00'),
            meal_amount=Decimal('50.00'),
            cash=Decimal('100.00'),
        ),
    ]
    user_repository.list_users.return_value = mock_users

    result = await user_use_case.list_all_users()

    expect_len_users = 2

    assert isinstance(result, UserListSchema)
    assert result.users == mock_users
    assert len(result.users) == expect_len_users
    user_repository.list_users.assert_called_once()


@pytest.mark.asyncio
async def test_list_all_users_empty(user_repository, user_use_case):
    user_repository.list_users.return_value = None

    result = await user_use_case.list_all_users()

    assert isinstance(result, UserListSchema)
    assert result.users == []
    assert len(result.users) == 0
    user_repository.list_users.assert_called_once()


@pytest.mark.asyncio
async def test_list_all_users_empty_list(user_repository, user_use_case):
    user_repository.list_users.return_value = []

    result = await user_use_case.list_all_users()

    assert isinstance(result, UserListSchema)
    assert result.users == []
    assert len(result.users) == 0
    user_repository.list_users.assert_called_once()


@pytest.mark.asyncio
async def test_update_user_success(
    user_repository, user_use_case, user_model, user_schema
):
    updated_user = user_schema
    user_repository.update_user.return_value = updated_user

    result = await user_use_case.update_user(user_model, user_schema)

    assert result == updated_user
    user_repository.update_user.assert_called_once()

    call_args = user_repository.update_user.call_args
    assert call_args[1]['current_user'] == user_model
    assert isinstance(call_args[1]['user'], UserDTO)


@pytest.mark.asyncio
async def test_update_balance_success_all_values(
    user_repository, user_use_case, user_schema
):
    user_repository.update_balance.return_value = user_schema

    food_amount = Decimal('100.50')
    meal_amount = Decimal('75.25')
    cash = Decimal('200.00')

    result = await user_use_case.update_balance(
        user_id=1, food_amount=food_amount, meal_amount=meal_amount, cash=cash
    )

    assert result == user_schema
    user_repository.update_balance.assert_called_once()

    call_args = user_repository.update_balance.call_args
    assert call_args[1]['user_id'] == 1
    balance_dto = call_args[1]['balance']
    assert isinstance(balance_dto, BalanceDTO)
    assert balance_dto.food_amount == food_amount
    assert balance_dto.meal_amount == meal_amount
    assert balance_dto.cash == cash


@pytest.mark.asyncio
async def test_update_balance_success_partial_values(
    user_repository, user_use_case, user_schema
):
    user_repository.update_balance.return_value = user_schema

    food_amount = Decimal('50.00')

    result = await user_use_case.update_balance(
        user_id=1, food_amount=food_amount, meal_amount=None, cash=None
    )

    assert result == user_schema
    user_repository.update_balance.assert_called_once()

    call_args = user_repository.update_balance.call_args
    balance_dto = call_args[1]['balance']
    assert balance_dto.food_amount == food_amount
    assert balance_dto.meal_amount is None
    assert balance_dto.cash is None


@pytest.mark.asyncio
async def test_update_balance_negative_food_amount(
    user_repository, user_use_case
):
    with pytest.raises(HTTPException) as exc_info:
        await user_use_case.update_balance(
            user_id=1,
            food_amount=Decimal('-10.00'),
            meal_amount=None,
            cash=None,
        )

    assert exc_info.value.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert 'Invalid values' in exc_info.value.detail
    assert 'food_amount (-10.00)' in exc_info.value.detail
    user_repository.update_balance.assert_not_called()


@pytest.mark.asyncio
async def test_update_balance_negative_meal_amount(
    user_repository, user_use_case
):
    with pytest.raises(HTTPException) as exc_info:
        await user_use_case.update_balance(
            user_id=1,
            food_amount=None,
            meal_amount=Decimal('-5.50'),
            cash=None,
        )

    assert exc_info.value.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert 'Invalid values' in exc_info.value.detail
    assert 'meal_amount (-5.50)' in exc_info.value.detail
    user_repository.update_balance.assert_not_called()


@pytest.mark.asyncio
async def test_update_balance_negative_cash(user_repository, user_use_case):
    with pytest.raises(HTTPException) as exc_info:
        await user_use_case.update_balance(
            user_id=1,
            food_amount=None,
            meal_amount=None,
            cash=Decimal('-25.75'),
        )

    assert exc_info.value.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert 'Invalid values' in exc_info.value.detail
    assert 'cash (-25.75)' in exc_info.value.detail
    user_repository.update_balance.assert_not_called()


@pytest.mark.asyncio
async def test_update_balance_multiple_negative_values(
    user_repository, user_use_case
):
    with pytest.raises(HTTPException) as exc_info:
        await user_use_case.update_balance(
            user_id=1,
            food_amount=Decimal('-10.00'),
            meal_amount=Decimal('-5.50'),
            cash=Decimal('-25.75'),
        )

    assert exc_info.value.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert 'Invalid values' in exc_info.value.detail
    assert 'food_amount (-10.00)' in exc_info.value.detail
    assert 'meal_amount (-5.50)' in exc_info.value.detail
    assert 'cash (-25.75)' in exc_info.value.detail
    user_repository.update_balance.assert_not_called()


@pytest.mark.asyncio
async def test_update_balance_zero_values_allowed(
    user_repository, user_use_case, user_schema
):
    user_repository.update_balance.return_value = user_schema

    result = await user_use_case.update_balance(
        user_id=1,
        food_amount=Decimal('0.00'),
        meal_amount=Decimal('0.00'),
        cash=Decimal('0.00'),
    )

    assert result == user_schema
    user_repository.update_balance.assert_called_once()


@pytest.mark.asyncio
async def test_update_balance_all_none_values(
    user_repository, user_use_case, user_schema
):
    user_repository.update_balance.return_value = user_schema

    result = await user_use_case.update_balance(
        user_id=1, food_amount=None, meal_amount=None, cash=None
    )

    assert result == user_schema
    user_repository.update_balance.assert_called_once()

    call_args = user_repository.update_balance.call_args
    balance_dto = call_args[1]['balance']
    assert balance_dto.food_amount is None
    assert balance_dto.meal_amount is None
    assert balance_dto.cash is None


@pytest.mark.asyncio
async def test_update_balance_mixed_positive_negative(
    user_repository, user_use_case
):
    with pytest.raises(HTTPException) as exc_info:
        await user_use_case.update_balance(
            user_id=1,
            food_amount=Decimal('100.00'),
            meal_amount=Decimal('-50.00'),
            cash=Decimal('200.00'),
        )

    assert exc_info.value.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert 'meal_amount (-50.00)' in exc_info.value.detail
    assert 'food_amount' not in exc_info.value.detail
    assert 'cash' not in exc_info.value.detail
    user_repository.update_balance.assert_not_called()
