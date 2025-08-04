from unittest.mock import AsyncMock, MagicMock

import pytest

from dataseed.application.interfaces.user_repository_interface import (
    UserRepositoryInterface,
)
from dataseed.application.use_cases.auth_use_case import AuthUseCase


@pytest.fixture
def user_repository():
    user_repository_mock = MagicMock(spec=UserRepositoryInterface)
    user_repository_mock.get_user_by_email = AsyncMock()

    return user_repository_mock


@pytest.fixture
def auth_use_case(user_repository):
    return AuthUseCase(user_repository)


@pytest.mark.asyncio
async def test_authenticate_user(user_repository, user, auth_use_case):
    user_repository.get_user_by_email.return_value = user

    result = await auth_use_case.authenticate_user(
        email=user.email, password=user.clean_password
    )

    assert result is not None
    assert result.token_type == 'Bearer'
    assert result.access_token is not None

    user_repository.get_user_by_email.assert_called_once_with(user.email)


@pytest.mark.asyncio
async def test_create_token(user_repository, user, auth_use_case):
    result = auth_use_case.create_token(user=user)

    assert result is not None
    assert result.token_type == 'Bearer'
    assert result.access_token is not None


@pytest.mark.asyncio
async def test_refresh_token(user_repository, user, auth_use_case):
    result = auth_use_case.refresh_user_token(user=user)

    assert result is not None
    assert result.token_type == 'Bearer'
    assert result.access_token is not None
