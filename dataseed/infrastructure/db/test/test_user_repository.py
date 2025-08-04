import pytest
from sqlalchemy import select

from dataseed.models import User as UserModel


@pytest.mark.asyncio
async def test_create_user(session):
    new_user = UserModel(
        username='Alice', password='secret', email='test@test.com'
    )
    session.add(new_user)
    await session.commit()

    user = await session.scalar(
        select(UserModel).where(UserModel.username == 'Alice')
    )

    assert user.username == new_user.username


@pytest.mark.asyncio
async def test_get_user_by_email(session):
    new_user = UserModel(
        username='Alice', password='secret', email='test@test.com'
    )
    session.add(new_user)
    await session.commit()

    user = await session.scalar(
        select(UserModel).where(UserModel.email == 'test@test.com')
    )

    assert user.username == 'Alice'


@pytest.mark.asyncio
async def test_list_users(session):
    new_user = UserModel(username='Anne', password='123', email='a@a.com')
    session.add(new_user)
    new_user = UserModel(username='Vitor', password='456', email='b@b.com')
    session.add(new_user)
    new_user = UserModel(username='Leidy', password='789', email='c@c.com')
    session.add(new_user)
    await session.commit()

    result = await session.scalars(select(UserModel))
    users = result.all()

    expected_len_users = 3

    assert users[0].username == 'Anne'
    assert len(users) == expected_len_users
