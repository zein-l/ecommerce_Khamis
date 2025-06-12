from memory_profiler import profile
from inventory.app import create_app as create_inventory_app

# Create app instance for the inventory service
inventory_app = create_inventory_app()

# -------------------------
# Memory Profiling Functions
# -------------------------

@profile
def test_create_product():
    """
    Test memory usage for creating a new product.
    """
    with inventory_app.test_client() as client:
        response = client.post('/products', json={
            "name": "Memory Test Product",
            "description": "This is a test product for memory profiling.",
            "price": 25.99,
            "quantity": 100
        })
        print(f"Create Product Response: {response.get_json()}")


@profile
def test_get_all_products():
    """
    Test memory usage for retrieving all products.
    """
    with inventory_app.test_client() as client:
        response = client.get('/products')
        print(f"Get All Products Response: {response.get_json()}")


@profile
def test_get_product_by_id():
    """
    Test memory usage for retrieving a product by ID.
    """
    with inventory_app.test_client() as client:
        # Assuming product ID 1 exists for testing purposes
        response = client.get('/products/1')
        print(f"Get Product by ID Response: {response.get_json()}")


@profile
def test_update_product():
    """
    Test memory usage for updating a product.
    """
    with inventory_app.test_client() as client:
        # Assuming product ID 1 exists for testing purposes
        response = client.put('/products/1', json={
            "name": "Updated Test Product",
            "description": "Updated description for memory profiling.",
            "price": 30.99,
            "quantity": 200
        })
        print(f"Update Product Response: {response.get_json()}")


@profile
def test_delete_product():
    """
    Test memory usage for deleting a product.
    """
    with inventory_app.test_client() as client:
        # Assuming product ID 1 exists for testing purposes
        response = client.delete('/products/1')
        print(f"Delete Product Response: {response.get_json()}")


if __name__ == "__main__":
    # Run memory profiling for the Inventory service
    test_create_product()
    test_get_all_products()
    test_get_product_by_id()
    test_update_product()
    test_delete_product()
