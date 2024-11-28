import pytest
from customers.app import create_app
from customers.app.db import db



@pytest.fixture
def client():
    """
    Fixture to set up the test client and an in-memory SQLite database.
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


import uuid  

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
    if response.status_code != 201:
        print(response.get_json())
    assert response.status_code == 201, "Expected status code 201 for successful registration"
    assert response.get_json()['message'] == "Customer registered successfully."


def test_duplicate_username(client):
    """
    Test registration with a duplicate username.
    """
    # Register the first customer
    client.post('/customers/register', json={
        "full_name": "Jane Smith",
        "username": "janesmith",
        "password": "StrongPass!23",
        "age": 28,
        "address": "456 Elm St, Anytown, USA"
    })

    # Attempt to register another customer with the same username
    response = client.post('/customers/register', json={
        "full_name": "Jane Smith",
        "username": "janesmith",
        "password": "AnotherPass!23",
        "age": 28,
        "address": "456 Elm St, Anytown, USA"
    })
    assert response.status_code == 400, "Expected status code 400 for duplicate username"
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
    assert response.status_code == 400, "Expected status code 400 for invalid age"
    assert "Must be greater than or equal to 1." in response.get_json()['details']['age'], \
        "Error message does not match the expected validation output."


def test_missing_fields(client):
    """
    Test registration with missing required fields.
    """
    response = client.post('/customers/register', json={
        "username": "alicewilliams",
        "password": "AlicePass!23",
        "age": 32
    })
    assert response.status_code == 400, "Expected status code 400 for missing fields"
    assert "full_name" in response.get_json()['details']
    assert "address" in response.get_json()['details']


def test_invalid_username_length(client):
    """
    Test registration with an invalid (short) username.
    """
    response = client.post('/customers/register', json={
        "full_name": "Invalid User",
        "username": "",
        "password": "ValidPass!23",
        "age": 25,
        "address": "123 Main St, Anytown, USA",
        "gender": "Other",
        "marital_status": "Single"
    })
    assert response.status_code == 400, "Expected status code 400 for invalid username length"
    assert "username" in response.get_json()['details']


def test_delete_customer(client):
    """
    Test deleting a customer by username.
    """
    # First, create a test customer
    client.post('/customers/register', json={
        "full_name": "Test User",
        "username": "testuser",
        "password": "TestPass123!",
        "age": 25,
        "address": "Test Address",
        "gender": "Male",
        "marital_status": "Single"
    })

    # Delete the test customer
    response = client.delete('/customers/testuser')
    assert response.status_code == 200
    assert response.get_json()['message'] == "Customer 'testuser' deleted successfully."

    # Try to delete again to ensure proper error handling
    response = client.delete('/customers/testuser')
    assert response.status_code == 404
    assert response.get_json()['error'] == "Customer with username 'testuser' not found."


def test_get_all_customers(client):
    """
    Test retrieving all customers.
    """
    # Add the first customer
    client.post('/customers/register', json={
        "full_name": "John Doe",
        "username": "johndoe",
        "password": "SecurePass123!",
        "age": 30,
        "address": "123 Main St",
        "gender": "Male",
        "marital_status": "Single"
    })

    # Add the second customer
    client.post('/customers/register', json={
        "full_name": "Jane Doe",
        "username": "janedoe",
        "password": "SecurePass123!",
        "age": 28,
        "address": "456 Elm St",
        "gender": "Female",
        "marital_status": "Married"
    })

    # Get all customers
    response = client.get('/customers')
    assert response.status_code == 200, "Expected 200 OK status for retrieving customers"

    # Extract data from response
    data = response.get_json()
    print("Response Data:", data)  # Debugging

    # Validate specific customer details
    usernames = [customer['username'] for customer in data]
    assert "johndoe" in usernames, "Expected username 'johndoe' not found in response"
    assert "janedoe" in usernames, "Expected username 'janedoe' not found in response"


# tests/test_update_customer.py
def test_update_customer(client):
    client.post('/customers/register', json={
        "full_name": "John Doe",
        "username": "johndoe",
        "password": "SecurePass123!",
        "age": 30,
        "address": "123 Main St",
        "gender": "Male",
        "marital_status": "Single"
    })

    response = client.put('/customers/johndoe', json={
        "age": 31,
        "address": "789 Pine St"
    })
    assert response.status_code == 200
    assert "updated successfully" in response.get_json()['message']

    # Confirm changes
    response = client.get('/customers/johndoe')
    assert response.status_code == 200
    data = response.get_json()
    assert data['age'] == 31
    assert data['address'] == "789 Pine St"


import uuid

def test_wallet_operations(client):
    # Generate a unique username
    unique_username = f"user_{uuid.uuid4().hex[:8]}"  # Unique username with 8 characters from UUID

    # Register a customer
    response = client.post('/customers/register', json={
        "full_name": "John Doe",
        "username": unique_username,
        "password": "SecurePass123!",
        "age": 30,
        "address": "123 Main St",
        "gender": "Male",
        "marital_status": "Single"
    })
    if response.status_code != 201:
        print("Registration Error Response:", response.get_json())  # Debugging output
    assert response.status_code == 201

    # Charge wallet
    response = client.post(f'/customers/{unique_username}/charge', json={"amount": 100.0})
    charge_response = response.get_json()
    assert response.status_code == 200
    assert charge_response['new_balance'] == 100.0
