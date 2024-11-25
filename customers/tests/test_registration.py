def test_successful_registration(client):
    response = client.post('/customers/register', json={
        "full_name": "Jane Smith",
        "username": "janesmith",
        "password": "StrongPass!23",
        "age": 28,
        "address": "456 Elm St, Anytown, USA"
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == "Customer registered successfully."


def test_duplicate_username(client):
    # Assume 'janesmith' is already registered
    response = client.post('/customers/register', json={
        "full_name": "Jane Smith",
        "username": "janesmith",
        "password": "AnotherPass!23",
        "age": 28,
        "address": "456 Elm St, Anytown, USA"
    })
    assert response.status_code == 400
    assert "Username 'janesmith' is already taken." in response.get_json()['error']


def test_invalid_age(client):
    response = client.post('/customers/register', json={
        "full_name": "Bob Johnson",
        "username": "bobjohnson",
        "password": "Pass123!",
        "age": -5,
        "address": "789 Pine St, Anytown, USA"
    })
    assert response.status_code == 400
    assert "Age must be a positive integer." in response.get_json()['details']['age']


def test_missing_fields(client):
    response = client.post('/customers/register', json={
        "username": "alicewilliams",
        "password": "AlicePass!23",
        "age": 32
    })
    assert response.status_code == 400
    assert "full_name" in response.get_json()['details']
    assert "address" in response.get_json()['details']


