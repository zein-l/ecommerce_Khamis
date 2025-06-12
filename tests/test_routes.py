import pytest
from customers.app import create_app
from customers.app.db import db
import uuid
import os

@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create SQLite tables
        yield client
        with app.app_context():
            db.session.remove()
            db.get_engine().dispose()  # Close connection
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'


def test_register_customer(client):
    """
    Test successful customer registration with valid data.
    """
    unique_username = f"johnd_{uuid.uuid4().hex[:6]}"  # Generate a unique username
    response = client.post('/customers/register', json={
        "full_name": "John Doe",
        "username": unique_username,
        "password": "SecurePass123!",
        "age": 30,
        "address": "123 Main St",
        "gender": "Male",
        "marital_status": "Single"
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == "Customer registered successfully."


def test_duplicate_username(client):
    """
    Test registration with a duplicate username.
    """
    client.post('/customers/register', json={
        "full_name": "Jane Smith",
        "username": "janesmith",
        "password": "StrongPass!23",
        "age": 28,
        "address": "456 Elm St, Anytown, USA"
    })

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
    """
    Test registration with an invalid (negative) age.
    """
    response = client.post('/customers/register', json={
        "full_name": "Bob Johnson",
        "username": "bobjohnson",
        "password": "Pass123!",
        "age": -5,
        "address": "789 Pine St, Anytown, USA"
    })
    assert response.status_code == 400


def test_missing_fields(client):
    """
    Test registration with missing required fields.
    """
    response = client.post('/customers/register', json={
        "username": "alicewilliams",
        "password": "AlicePass!23",
        "age": 32
    })
    assert response.status_code == 400


def test_delete_customer(client):
    """
    Test deleting a customer by username.
    """
    client.post('/customers/register', json={
        "full_name": "Test User",
        "username": "testuser",
        "password": "TestPass123!",
        "age": 25,
        "address": "Test Address",
        "gender": "Male",
        "marital_status": "Single"
    })

    response = client.delete('/customers/testuser')
    assert response.status_code == 200
    assert response.get_json()['message'] == "Customer 'testuser' deleted successfully."
