# from http import HTTPStatus
#
#
# def test_add_balance_food_amount_should_return_updated_user(
#     client, user, token
# ):
#     old_food_amount = user.food_amount
#     food_amount_plus = 100.00
#
#     response = client.put(
#         f'/management/add_balance_in_account/{user.id}',
#         headers={'Authorization': f'Bearer {token}'},
#         json={'food_amount': food_amount_plus},
#     )
#
#     assert response.status_code == HTTPStatus.OK
#     data = response.json()
#     assert data['food_amount'] == float(old_food_amount) +
#     data['food_amount']
#     assert 'id' in data
#     assert 'email' in data
#
#
# def test_add_balance_meal_amount_should_return_updated_user(
#     client, user, token
# ):
#     response = client.put(
#         f'/management/add_balance_in_account/{user.id}',
#         headers={'Authorization': f'Bearer {token}'},
#         json={'meal_amount': 50.00},
#     )
#
#     assert response.status_code == HTTPStatus.OK
#     data = response.json()
#     assert data['meal_amount'] == '50.00'
#     assert 'id' in data
#     assert 'email' in data
#
#
# def test_add_balance_cash_should_return_updated_user(client, user, token):
#     response = client.put(
#         f'/management/add_balance_in_account/{user.id}',
#         headers={'Authorization': f'Bearer {token}'},
#         json={'cash': 75.00},
#     )
#
#     assert response.status_code == HTTPStatus.OK
#     data = response.json()
#     assert data['cash'] == '75.00'
#     assert 'id' in data
#     assert 'email' in data
#
#
# def test_add_balance_multiple_values_should_return_updated_user(
#     client, user, token
# ):
#     response = client.put(
#         f'/management/add_balance_in_account/{user.id}',
#         headers={'Authorization': f'Bearer {token}'},
#         json={'food_amount': 100.00, 'meal_amount': 50.00, 'cash': 75.00},
#     )
#
#     assert response.status_code == HTTPStatus.OK
#     data = response.json()
#     assert data['food_amount'] == '100.00'
#     assert data['meal_amount'] == '50.00'
#     assert data['cash'] == '75.00'
#     assert 'id' in data
#     assert 'email' in data
#
#
# def test_add_balance_invalid_user_id_should_return_not_found(client, token):
#     response = client.put(
#         '/management/add_balance_in_account/999999',
#         headers={'Authorization': f'Bearer {token}'},
#         json={'food_amount': 100.00},
#     )
#
#     assert response.status_code == HTTPStatus.NOT_FOUND
#
#
# def test_add_balance_without_token_should_return_unauthorized(client, user):
#     response = client.put(
#         f'/management/add_balance_in_account/{user.id}',
#         json={'food_amount': 100.00},
#     )
#
#     assert response.status_code == HTTPStatus.UNAUTHORIZED
