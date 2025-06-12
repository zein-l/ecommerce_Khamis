import pytest
from sales.app import create_app
from sales.app.db import db

@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create in-memory tables
        yield client
        with app.app_context():
            db.session.remove()
            db.get_engine().dispose()

def test_create_sale(client):
    """Test creating a sale record."""
    response = client.post('/sales', json={
        "product_id": 1,
        "quantity": 2,
        "total_price": 49.98,
        "customer_id": 3
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == "Sale created successfully"  # Updated expected message


def test_get_sales(client):
    """Test retrieving all sales."""
    response = client.get('/sales')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_sale_by_id(client):
    """Test retrieving a sale by ID."""
    # Add a sale first
    response = client.post('/sales', json={
        "product_id": 1,
        "quantity": 2,
        "total_price": 49.98,
        "customer_id": 3
    })
    sale_id = response.get_json()['sale_id']

    # Retrieve the sale
    response = client.get(f'/sales/{sale_id}')
    assert response.status_code == 200
    sale = response.get_json()
    assert sale['product_id'] == 1
    assert sale['quantity'] == 2
    assert sale['total_price'] == 49.98
    assert sale['customer_id'] == 3
