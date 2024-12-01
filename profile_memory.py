from memory_profiler import profile
from customers.app import create_app as create_customers_app
from inventory.app import create_app as create_inventory_app

# Create app instances for both services
customer_app = create_customers_app()
inventory_app = create_inventory_app()

# Customer Service Memory Profiling
@profile
def test_register_customer():
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
    with customer_app.test_client() as client:
        response = client.get('/customers')
        print(f"Get All Customers Response: {response.get_json()}")

@profile
def test_get_customer_by_username():
    with customer_app.test_client() as client:
        response = client.get('/customers/memorytestuser')
        print(f"Get Customer by Username Response: {response.get_json()}")

@profile
def test_update_customer():
    with customer_app.test_client() as client:
        response = client.put('/customers/memorytestuser', json={
            "address": "456 Updated St",
            "age": 31
        })
        print(f"Update Customer Response: {response.get_json()}")

@profile
def test_delete_customer():
    with customer_app.test_client() as client:
        response = client.delete('/customers/memorytestuser')
        print(f"Delete Customer Response: {response.get_json()}")

@profile
def test_charge_wallet():
    with customer_app.test_client() as client:
        response = client.post('/customers/memorytestuser/charge', json={
            "amount": 100.0
        })
        print(f"Charge Wallet Response: {response.get_json()}")

@profile
def test_deduct_wallet():
    with customer_app.test_client() as client:
        response = client.post('/customers/memorytestuser/deduct', json={
            "amount": 50.0
        })
        print(f"Deduct Wallet Response: {response.get_json()}")

# Inventory Service Memory Profiling
@profile
def test_create_product():
    with inventory_app.test_client() as client:
        response = client.post('/products', json={
            "name": "Test Product",
            "description": "Performance test product",
            "price": 10.99,
            "quantity": 5
        })
        print(f"Create Product Response: {response.get_json()}")

@profile
def test_get_all_products():
    with inventory_app.test_client() as client:
        response = client.get('/products')
        print(f"Get All Products Response: {response.get_json()}")

@profile
def test_get_product_by_id():
    with inventory_app.test_client() as client:
        # Assuming product ID 1 exists for testing purposes
        response = client.get('/products/1')
        print(f"Get Product by ID Response: {response.get_json()}")

@profile
def test_update_product():
    with inventory_app.test_client() as client:
        # Assuming product ID 1 exists for testing purposes
        response = client.put('/products/1', json={
            "name": "Updated Product",
            "description": "Updated description",
            "price": 15.99,
            "quantity": 10
        })
        print(f"Update Product Response: {response.get_json()}")

@profile
def test_delete_product():
    with inventory_app.test_client() as client:
        # Assuming product ID 1 exists for testing purposes
        response = client.delete('/products/1')
        print(f"Delete Product Response: {response.get_json()}")

if __name__ == "__main__":
    # Customer Service Tests
    test_register_customer()
    test_get_all_customers()
    test_get_customer_by_username()
    test_update_customer()
    test_charge_wallet()
    test_deduct_wallet()
    test_delete_customer()

    # Inventory Service Tests
    test_create_product()
    test_get_all_products()
    test_get_product_by_id()
    test_update_product()
    test_delete_product()
