import cProfile
from pstats import Stats
from memory_profiler import profile
from customers.app import create_app as create_customers_app
from customers.app.db import db as customers_db
from inventory.app import create_app as create_inventory_app
from inventory.app.db import db as inventory_db
from sales.app import create_app as create_sales_app
from sales.app.db import db as sales_db


# -------------------------
# Utility Functions
# -------------------------

def setup_app(app, db_instance):
    """
    Configure the Flask app to use SQLite in-memory and initialize the database.
    """
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'TESTING': True,
    })
    with app.app_context():
        db_instance.create_all()


# -------------------------
# Profiling Test Functions
# -------------------------

@profile
def test_customer_service():
    """
    Tests for the Customer Service endpoints.
    """
    customer_app = create_customers_app()
    setup_app(customer_app, customers_db)

    with customer_app.test_client() as client:
        # Test Register
        client.post('/customers/register', json={
            "full_name": "Memory Test User",
            "username": "memorytestuser",
            "password": "Test123!",
            "age": 30,
            "address": "123 Memory Lane",
            "gender": "Male",
            "marital_status": "Single",
        })

        # Test Get All Customers
        client.get('/customers')

        # Test Delete Customer
        client.delete('/customers/memorytestuser')


@profile
def test_inventory_service():
    """
    Tests for the Inventory Service endpoints.
    """
    inventory_app = create_inventory_app()
    setup_app(inventory_app, inventory_db)

    with inventory_app.test_client() as client:
        # Test Create Product
        client.post('/products', json={
            "name": "Test Product",
            "description": "Performance test product",
            "price": 10.99,
            "quantity": 5,
        })

        # Test Get All Products
        client.get('/products')

        # Test Delete Product
        client.delete('/products/1')


@profile
def test_sales_service():
    """
    Tests for the Sales Service endpoints.
    """
    sales_app = create_sales_app()
    setup_app(sales_app, sales_db)

    with sales_app.test_client() as client:
        # Test Create Sale
        client.post('/sales', json={
            "product_id": 1,
            "quantity": 2,
            "total_price": 49.98,
            "customer_id": 3,
        })

        # Test Get All Sales
        client.get('/sales')

        # Test Delete Sale
        client.delete('/sales/1')


# -------------------------
# Performance Profiling
# -------------------------

def profile_performance():
    """
    Run performance profiling with cProfile.
    """
    profiler = cProfile.Profile()
    profiler.enable()

    # Run test functions
    test_customer_service()
    test_inventory_service()
    test_sales_service()

    profiler.disable()
    stats = Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats("cumtime")
    stats.print_stats()


# -------------------------
# Main Execution
# -------------------------

if __name__ == "__main__":
    print("Memory and Performance Profiling...")
    profile_performance()
