from decimal import Decimal
from http import HTTPStatus


def test_add_balance_food_amount_should_return_updated_user(
    client, user, token
):
    old_food_amount = user.food_amount
    food_amount_plus = 100.00

    response = client.put(
        f'/management/add_balance_in_account/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        params={'food_amount': food_amount_plus},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert food_amount_plus == Decimal(data['food_amount']) - old_food_amount
    assert 'id' in data
    assert 'email' in data


def test_add_balance_meal_amount_should_return_updated_user(
    client, user, token
):
    old_meal_amount = user.meal_amount
    meal_amount_plus = 50.00

    response = client.put(
        f'/management/add_balance_in_account/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        params={'meal_amount': meal_amount_plus},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert meal_amount_plus == Decimal(data['meal_amount']) - old_meal_amount
    assert 'id' in data
    assert 'email' in data


def test_add_balance_cash_should_return_updated_user(client, user, token):
    old_cash = user.cash
    cash_plus = 75.00

    response = client.put(
        f'/management/add_balance_in_account/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        params={'cash': cash_plus},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert cash_plus == Decimal(data['cash']) - old_cash
    assert 'id' in data
    assert 'email' in data


def test_add_balance_multiple_values_should_return_updated_user(
    client, user, token
):
    old_food_amount = user.food_amount
    food_amount_plus = 100.00
    old_meal_amount = user.meal_amount
    meal_amount_plus = 50.00
    old_cash = user.cash
    cash_plus = 75.00

    response = client.put(
        f'/management/add_balance_in_account/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        params={
            'food_amount': food_amount_plus,
            'meal_amount': meal_amount_plus,
            'cash': cash_plus,
        },
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert food_amount_plus == Decimal(data['food_amount']) - old_food_amount
    assert meal_amount_plus == Decimal(data['meal_amount']) - old_meal_amount
    assert cash_plus == Decimal(data['cash']) - old_cash
    assert 'id' in data
    assert 'email' in data


def test_add_balance_invalid_user_id_should_return_not_found(client, token):
    response = client.put(
        '/management/add_balance_in_account/999999',
        headers={'Authorization': f'Bearer {token}'},
        params={'food_amount': 100.00},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
