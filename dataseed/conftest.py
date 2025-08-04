import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from dataseed import security
from dataseed.app import app
from dataseed.database import get_session
from dataseed.models import User, table_registry


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@email.com')
    password = factory.LazyAttribute(
        lambda obj: security.get_password_hash(f'{obj.username}-passwd')
    )
    food_amount = factory.Faker(
        'pydecimal', left_digits=3, right_digits=2, positive=True
    )
    meal_amount = factory.Faker(
        'pydecimal', left_digits=3, right_digits=2, positive=True
    )
    cash = factory.Faker(
        'pydecimal', left_digits=4, right_digits=2, positive=True
    )


@pytest.fixture(scope='session')
async def engine():
    engine = create_async_engine('sqlite+aiosqlite:///:memory:')
    yield engine
    await engine.dispose()


@pytest.fixture
async def session(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def user(session: AsyncSession):
    password = 'passwd'
    user = UserFactory(password=security.get_password_hash(password))
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
async def other_user(session: AsyncSession):
    password = 'passwd'
    user = UserFactory(password=security.get_password_hash(password))
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']


@pytest.fixture
def invalid_token():
    data = {'sub': 'invalid_username@email.com'}
    return security.create_access_token(data)


@pytest.fixture
def no_valid_field_token():
    data = {'iss': 'invalid_username@email.com'}
    return security.create_access_token(data)


@pytest.fixture
def user_data():
    return {
        'username': 'teste',
        'email': 'testuser@example.com',
        'password': 'testpassword123',
    }


@pytest.fixture
def transaction_data(user):
    return {
        'account': str(user.id),
        'amount': 10.50,
        'mcc': '5411',
        'merchant': 'PADARIA DO ZE               SAO PAULO BR',
    }


@pytest.fixture
def insufficient_balance_transaction(user):
    return {
        'account': str(user.id),
        'amount': 1000.00,
        'mcc': '5411',
        'merchant': 'LOJA CARA                  SAO PAULO BR',
    }


@pytest.fixture
def invalid_merchant_transaction(user):
    return {
        'account': str(user.id),
        'amount': 10.00,
        'mcc': '5411',
        'merchant': 'MERCHANT_INVALIDO',
    }


@pytest.fixture
def nonexistent_user_transaction():
    return {
        'account': '99999',
        'amount': 10.00,
        'mcc': '5411',
        'merchant': 'MERCHANT TEST               SAO PAULO BR',
    }
