from locust import HttpUser, task, between

class CustomerServiceUser(HttpUser):
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
