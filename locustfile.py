from locust import HttpUser, task, between

class CustomerServiceUser(HttpUser):
    # Base URL for the Customer Service
    host = "http://127.0.0.1:5001"
    wait_time = between(1, 2)

    @task
    def get_all_customers(self):
        self.client.get("/customers")

    @task
    def register_customer(self):
        self.client.post("/customers/register", json={
            "full_name": "Test User",
            "username": "testuser",
            "password": "Test123!",
            "age": 30,
            "address": "123 Test St",
            "gender": "Male",
            "marital_status": "Single"
        })

    @task
    def update_customer(self):
        self.client.put("/customers/testuser", json={
            "address": "456 Updated St",
            "age": 31
        })

    @task
    def delete_customer(self):
        self.client.delete("/customers/testuser")

    @task
    def get_customer_by_username(self):
        self.client.get("/customers/testuser")

    @task
    def charge_wallet(self):
        self.client.post("/customers/testuser/charge", json={"amount": 50.0})

    @task
    def deduct_wallet(self):
        self.client.post("/customers/testuser/deduct", json={"amount": 20.0})


class InventoryServiceUser(HttpUser):
    # Base URL for the Inventory Service
    host = "http://127.0.0.1:5002"  # Adjust port if different for inventory service
    wait_time = between(1, 2)

    @task
    def get_all_products(self):
        self.client.get("/products")

    @task
    def create_product(self):
        self.client.post("/products", json={
            "name": "Test Product",
            "description": "Performance test product",
            "price": 10.99,
            "quantity": 5
        })

    @task
    def update_product(self):
        # Assuming product ID 1 exists for testing purposes
        self.client.put("/products/1", json={
            "name": "Updated Product",
            "description": "Updated description",
            "price": 15.99,
            "quantity": 10
        })

    @task
    def delete_product(self):
        # Assuming product ID 1 exists for testing purposes
        self.client.delete("/products/1")

    @task
    def get_product_by_id(self):
        # Assuming product ID 1 exists for testing purposes
        self.client.get("/products/1")


class SalesServiceUser(HttpUser):
    wait_time = between(1, 3)  # Simulate a wait time between tasks
    host = "http://127.0.0.1:5003"

    @task
    def create_sale(self):
        """Simulate creating a sale."""
        self.client.post("/sales", json={
            "product_id": 1,
            "quantity": 2,
            "total_price": 49.98,
            "customer_id": 3
        })

    @task
    def get_sales(self):
        """Simulate retrieving all sales."""
        self.client.get("/sales")

    @task
    def get_sale_by_id(self):
        """Simulate retrieving a specific sale by ID."""
        self.client.get("/sales/1")


class ReviewsServiceUser(HttpUser):
    wait_time = between(1, 2)  # Simulate a wait time between tasks
    host = "http://127.0.0.1:5004"

    @task
    def create_review(self):
        """Simulate creating a review."""
        self.client.post("/reviews/", json={
            "product_id": 1,
            "customer_id": 2,
            "rating": 5,
            "comment": "Amazing product!"
        })

    @task
    def get_review_by_id(self):
        """Simulate retrieving a specific review by ID."""
        self.client.get("/reviews/1")

    @task
    def get_reviews_by_product(self):
        """Simulate retrieving all reviews for a product."""
        self.client.get("/reviews/product/1")

    @task
    def get_reviews_by_customer(self):
        """Simulate retrieving all reviews for a customer."""
        self.client.get("/reviews/customer/2")

    @task
    def update_review(self):
        """Simulate updating a review."""
        self.client.put("/reviews/1", json={
            "rating": 4,
            "comment": "Updated review comment."
        })

    @task
    def delete_review(self):
        """Simulate deleting a review."""
        self.client.delete("/reviews/1")
