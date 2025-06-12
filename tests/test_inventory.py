import pytest
from inventory.app import create_app
from inventory.app.db import db
from inventory.app.models import Product
import os

@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    print("Using database URI:", app.config['SQLALCHEMY_DATABASE_URI'])  
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create SQLite tables
        yield client
        with app.app_context():
            db.session.remove()
            db.get_engine().dispose()  # Close connection

os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

def test_create_product(client):
    """
    Test creating a product.
    """
    response = client.post('/products', json={
        "name": "Sample Product",
        "description": "This is a test product",
        "price": 19.99,
        "quantity": 10
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == "Product created successfully"


def test_get_products(client):
    """
    Test retrieving all products.
    """
    # Add a product first
    client.post('/products', json={
        "name": "Sample Product",
        "description": "This is a test product",
        "price": 19.99,
        "quantity": 10
    })

    response = client.get('/products')
    assert response.status_code == 200
    products = response.get_json()
    assert len(products) == 1
    assert products[0]['name'] == "Sample Product"


def test_get_product_by_id(client):
    """
    Test retrieving a single product by ID.
    """
    # Add a product first
    response = client.post('/products', json={
        "name": "Sample Product",
        "description": "This is a test product",
        "price": 19.99,
        "quantity": 10
    })
    product_id = response.get_json()['product']

    # Retrieve the product
    response = client.get(f'/products/{product_id}')
    assert response.status_code == 200
    product = response.get_json()
    assert product['name'] == "Sample Product"


def test_update_product(client):
    """
    Test updating a product by ID.
    """
    # Add a product first
    response = client.post('/products', json={
        "name": "Sample Product",
        "description": "This is a test product",
        "price": 19.99,
        "quantity": 10
    })
    product_id = response.get_json()['product']

    # Update the product
    response = client.put(f'/products/{product_id}', json={
        "name": "Updated Product",
        "price": 29.99
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == "Product updated successfully"

    # Verify the update
    response = client.get(f'/products/{product_id}')
    product = response.get_json()
    assert product['name'] == "Updated Product"
    assert product['price'] == 29.99


def test_delete_product(client):
    """
    Test deleting a product by ID.
    """
    # Add a product first
    response = client.post('/products', json={
        "name": "Sample Product",
        "description": "This is a test product",
        "price": 19.99,
        "quantity": 10
    })
    product_id = response.get_json()['product']

    # Delete the product
    response = client.delete(f'/products/{product_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == "Product deleted successfully"

    # Verify the product no longer exists
    response = client.get(f'/products/{product_id}')
    assert response.status_code == 404
