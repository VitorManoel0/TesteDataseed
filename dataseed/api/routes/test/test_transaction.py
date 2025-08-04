from http import HTTPStatus


def test_process_transaction_should_return_success_response(
    client, user, transaction_data
):
    response = client.post('/transaction/authorizer', json=transaction_data)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'code' in data
    assert data['code'] == '00'


def test_process_transaction_insufficient_balance_should_return_error(
    client, user, insufficient_balance_transaction
):
    response = client.post(
        '/transaction/authorizer', json=insufficient_balance_transaction
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'code' in data
    assert data['code'] == '51'


def test_process_transaction_nonexistent_user_should_return_error(
    client, nonexistent_user_transaction
):
    response = client.post(
        '/transaction/authorizer', json=nonexistent_user_transaction
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'code' in data
    assert data['code'] == '07'


def test_process_transaction_missing_required_fields_should_return_error(
    client,
):
    incomplete_transaction = {
        'account': '123',
    }

    response = client.post(
        '/transaction/authorizer', json=incomplete_transaction
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_process_food_transaction_should_deduct_from_food_balance(
    client, user
):
    food_transaction = {
        'account': str(user.id),
        'amount': 25.00,
        'mcc': '5411',
        'merchant': 'SUPERMERCADO ABC            SAO PAULO BR',
    }

    response = client.post('/transaction/authorizer', json=food_transaction)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['code'] == '00'


def test_process_meal_transaction_should_deduct_from_meal_balance(
    client, user
):
    meal_transaction = {
        'account': str(user.id),
        'amount': 15.00,
        'mcc': '5812',
        'merchant': 'RESTAURANTE XYZ             SAO PAULO BR',
    }

    response = client.post('/transaction/authorizer', json=meal_transaction)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['code'] == '00'


def test_process_cash_transaction_should_deduct_from_cash_balance(
    client, user
):
    cash_transaction = {
        'account': str(user.id),
        'amount': 50.00,
        'mcc': '1234',
        'merchant': 'LOJA GENERICA               SAO PAULO BR',
    }

    response = client.post('/transaction/authorizer', json=cash_transaction)

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['code'] == '00'


def test_process_transaction_with_zero_amount(client, user):
    zero_amount_transaction = {
        'account': str(user.id),
        'amount': 0.00,
        'mcc': '5411',
        'merchant': 'MERCHANT TEST               SAO PAULO BR',
    }

    response = client.post(
        '/transaction/authorizer', json=zero_amount_transaction
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['code'] == '00'


def test_process_transaction_with_invalid_account_format_should_return_error(
    client,
):
    invalid_account_transaction = {
        'account': 'invalid_account_id',
        'amount': 10.00,
        'mcc': '5411',
        'merchant': 'MERCHANT TEST               SAO PAULO BR',
    }

    response = client.post(
        '/transaction/authorizer', json=invalid_account_transaction
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
