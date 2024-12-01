from memory_profiler import profile
from sales.app import create_app
from sales.app.db import db

# Create app instance for Sales service
sales_app = create_app({
    'TESTING': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # Use SQLite for testing
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
})

# Initialize the database
with sales_app.app_context():
    db.create_all()

# Memory profiling for Sales service
@profile
def test_create_sale():
    """
    Test creating a new sale.
    """
    with sales_app.test_client() as client:
        response = client.post('/sales', json={
            "product_id": 1,
            "quantity": 2,
            "total_price": 49.98,
            "customer_id": 3
        })
        print(f"Create Sale Response: {response.get_json()}")

@profile
def test_get_all_sales():
    """
    Test fetching all sales.
    """
    with sales_app.test_client() as client:
        response = client.get('/sales')
        print(f"Get All Sales Response: {response.get_json()}")

@profile
def test_get_sale_by_id():
    """
    Test fetching a sale by ID.
    """
    with sales_app.test_client() as client:
        response = client.get('/sales/1')  # Assuming sale ID 1 exists
        print(f"Get Sale by ID Response: {response.get_json()}")

@profile
def test_update_sale():
    """
    Test updating an existing sale.
    """
    with sales_app.test_client() as client:
        response = client.put('/sales/1', json={
            "quantity": 3,
            "total_price": 74.97
        })  # Assuming sale ID 1 exists
        print(f"Update Sale Response: {response.get_json()}")

@profile
def test_delete_sale():
    """
    Test deleting a sale.
    """
    with sales_app.test_client() as client:
        response = client.delete('/sales/1')  # Assuming sale ID 1 exists
        print(f"Delete Sale Response: {response.get_json()}")

if __name__ == "__main__":
    # Run memory profiling tests
    test_create_sale()
    test_get_all_sales()
    test_get_sale_by_id()
    test_update_sale()
    test_delete_sale()
