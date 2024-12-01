from memory_profiler import profile
from reviews.app import create_app as create_reviews_app
from reviews.app.db import db

# Create the application instance
app = create_reviews_app({
    'TESTING': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
})

# Initialize database tables for testing
with app.app_context():
    db.create_all()

# ------------------------------
# Memory Profiling Functions
# ------------------------------

@profile
def test_create_review():
    with app.test_client() as client:
        response = client.post('/reviews/', json={
            "product_id": 1,
            "customer_id": 2,
            "rating": 5,
            "comment": "Amazing product!"
        })
        print(f"Create Review Response: {response.get_json()}")

@profile
def test_get_review():
    with app.test_client() as client:
        response = client.get('/reviews/1')
        print(f"Get Review Response: {response.get_json()}")

@profile
def test_get_reviews_by_product():
    with app.test_client() as client:
        response = client.get('/reviews/product/1')
        print(f"Get Reviews by Product Response: {response.get_json()}")

@profile
def test_get_reviews_by_customer():
    with app.test_client() as client:
        response = client.get('/reviews/customer/2')
        print(f"Get Reviews by Customer Response: {response.get_json()}")

@profile
def test_update_review():
    with app.test_client() as client:
        response = client.put('/reviews/1', json={
            "rating": 4,
            "comment": "Updated comment"
        })
        print(f"Update Review Response: {response.get_json()}")

@profile
def test_delete_review():
    with app.test_client() as client:
        response = client.delete('/reviews/1')
        print(f"Delete Review Response: {response.get_json()}")

@profile
def test_moderate_review():
    with app.test_client() as client:
        response = client.post('/reviews/moderate/1', json={
            "action": "flag"
        })
        print(f"Moderate Review Response: {response.get_json()}")

# ------------------------------
# Run Memory Profiling Tests
# ------------------------------
if __name__ == "__main__":
    # Run the test cases
    test_create_review()
    test_get_review()
    test_get_reviews_by_product()
    test_get_reviews_by_customer()
    test_update_review()
    test_delete_review()
    test_moderate_review()
