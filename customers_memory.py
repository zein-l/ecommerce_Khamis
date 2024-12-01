from memory_profiler import profile
from customers.app import create_app as create_customers_app

# Create app instance for the Customers service
customer_app = create_customers_app({
    'TESTING': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # Use SQLite for testing
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
})

# Memory profiling for Customers service routes
@profile
def test_register_customer():
    """
    Test registering a new customer.
    """
    with customer_app.test_client() as client:
        response = client.post('/customers/register', json={
            "full_name": "Memory Test User",
            "username": "memorytestuser",
            "password": "Test123!",
            "age": 30,
            "address": "123 Memory Lane",
            "gender": "Male",
            "marital_status": "Single"
        })
        print(f"Register Customer Response: {response.get_json()}")

@profile
def test_get_all_customers():
    """
    Test retrieving all customers.
    """
    with customer_app.test_client() as client:
        response = client.get('/customers')
        print(f"Get All Customers Response: {response.get_json()}")

@profile
def test_get_customer_by_username():
    """
    Test retrieving a customer by username.
    """
    with customer_app.test_client() as client:
        response = client.get('/customers/memorytestuser')
        print(f"Get Customer by Username Response: {response.get_json()}")

@profile
def test_update_customer():
    """
    Test updating an existing customer's details.
    """
    with customer_app.test_client() as client:
        response = client.put('/customers/memorytestuser', json={
            "address": "456 Updated St",
            "age": 31
        })
        print(f"Update Customer Response: {response.get_json()}")

@profile
def test_delete_customer():
    """
    Test deleting a customer by username.
    """
    with customer_app.test_client() as client:
        response = client.delete('/customers/memorytestuser')
        print(f"Delete Customer Response: {response.get_json()}")

@profile
def test_charge_wallet():
    """
    Test charging a customer's wallet.
    """
    with customer_app.test_client() as client:
        response = client.post('/customers/memorytestuser/charge', json={
            "amount": 100.0
        })
        print(f"Charge Wallet Response: {response.get_json()}")

@profile
def test_deduct_wallet():
    """
    Test deducting from a customer's wallet.
    """
    with customer_app.test_client() as client:
        response = client.post('/customers/memorytestuser/deduct', json={
            "amount": 50.0
        })
        print(f"Deduct Wallet Response: {response.get_json()}")

if __name__ == "__main__":
    # Memory profiling for Customers service
    test_register_customer()
    test_get_all_customers()
    test_get_customer_by_username()
    test_update_customer()
    test_charge_wallet()
    test_deduct_wallet()
    test_delete_customer()
