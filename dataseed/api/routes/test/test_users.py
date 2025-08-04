from http import HTTPStatus


def test_create_account_should_return_created_user(client, user_data):
    """Testa a criação de uma nova conta"""
    response = client.post('/accounts/', json=user_data)

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert 'id' in data
    assert 'email' in data
    assert data['email'] == user_data['email']


def test_create_account_with_invalid_data_should_return_validation_error(
    client,
):
    """Testa criação de conta com dados inválidos"""
    invalid_user_data = {
        'email': 'invalid-email',  # email inválido
        'password': '123',  # senha muito curta
    }

    response = client.post('/accounts/', json=invalid_user_data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_account_with_existing_email_should_return_conflict(
    client, user_data, user
):
    response = client.post(
        '/accounts/',
        json={
            'username': 'teste',
            'email': user.email,
            'password': 'newpassword123',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT


def test_get_all_accounts_should_return_users_list(client, user, token):
    response = client.get(
        '/accounts/get_all', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'users' in data
    assert len(data['users']) >= 1
    assert any(u['id'] == user.id for u in data['users'])


def test_get_all_accounts_without_auth_should_return_unauthorized(client):
    response = client.get('/accounts/get_all')

    assert response.status_code == HTTPStatus.OK


def test_update_user_should_return_updated_user(client, user, token):
    updated_data = {
        'username': 'newusername',
        'email': 'newemail@example.com',
        'password': 'newpassword123',
    }

    response = client.put(
        f'/accounts/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=updated_data,
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'id' in data
    assert 'email' in data
    assert data['id'] == user.id


def test_update_user_different_user_should_return_forbidden(
    client, user, token, other_user
):
    updated_data = {
        'username': 'newusername',
        'email': 'newemail@example.com',
        'password': 'newpassword123',
    }

    response = client.put(
        f'/accounts/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=updated_data,
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    data = response.json()
    assert data['detail'] == 'Not enough permission'


def test_update_user_without_auth_should_return_unauthorized(client, user):
    updated_data = {
        'email': 'newemail@example.com',
        'password': 'newpassword123',
    }

    response = client.put(f'/accounts/{user.id}', json=updated_data)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_update_user_with_invalid_data_should_return_validation_error(
    client, user, token
):
    invalid_data = {'email': 'invalid-email', 'password': '123'}

    response = client.put(
        f'/accounts/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=invalid_data,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_delete_user_should_return_success_message(client, user, token):
    response = client.delete(
        f'/accounts/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['message'] == 'User successfully removed'


def test_delete_user_different_user_should_return_forbidden(
    client, user, token, other_user
):
    response = client.delete(
        f'/accounts/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    data = response.json()
    assert data['detail'] == 'Not enough permission'


def test_delete_user_without_auth_should_return_unauthorized(client, user):
    response = client.delete(f'/accounts/{user.id}')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_nonexistent_user_should_return_not_found(client, token):
    nonexistent_user_id = 99999

    response = client.delete(
        f'/accounts/{nonexistent_user_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
