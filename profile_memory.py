from memory_profiler import profile
from customers.app import create_app

app = create_app()

@profile
def test_register_customer():
    with app.test_client() as client:
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
    with app.test_client() as client:
        response = client.get('/customers')
        print(f"Get All Customers Response: {response.get_json()}")

@profile
def test_get_customer_by_username():
    with app.test_client() as client:
        response = client.get('/customers/memorytestuser')
        print(f"Get Customer by Username Response: {response.get_json()}")

@profile
def test_update_customer():
    with app.test_client() as client:
        response = client.put('/customers/memorytestuser', json={
            "address": "456 Updated St",
            "age": 31
        })
        print(f"Update Customer Response: {response.get_json()}")

@profile
def test_delete_customer():
    with app.test_client() as client:
        response = client.delete('/customers/memorytestuser')
        print(f"Delete Customer Response: {response.get_json()}")

@profile
def test_charge_wallet():
    with app.test_client() as client:
        response = client.post('/customers/memorytestuser/charge', json={
            "amount": 100.0
        })
        print(f"Charge Wallet Response: {response.get_json()}")

@profile
def test_deduct_wallet():
    with app.test_client() as client:
        response = client.post('/customers/memorytestuser/deduct', json={
            "amount": 50.0
        })
        print(f"Deduct Wallet Response: {response.get_json()}")

if __name__ == "__main__":
    test_register_customer()
    test_get_all_customers()
    test_get_customer_by_username()
    test_update_customer()
    test_charge_wallet()
    test_deduct_wallet()
    test_delete_customer()
