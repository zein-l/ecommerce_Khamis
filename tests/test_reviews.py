import pytest
from reviews.app import create_app
from reviews.app.db import db

@pytest.fixture
def reviews_client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # Use SQLite for testing
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables for SQLite
        yield client
        with app.app_context():
            db.session.remove()
            db.get_engine().dispose()

def test_create_review_valid(reviews_client):
    response = reviews_client.post('/reviews/', json={
        "product_id": 1,
        "customer_id": 2,
        "rating": 5,
        "comment": "Excellent product!"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == "Review created successfully"
    assert data['review']['rating'] == 5

def test_create_review_invalid_rating(reviews_client):
    response = reviews_client.post('/reviews/', json={
        "product_id": 1,
        "customer_id": 2,
        "rating": 6,  # Invalid rating
        "comment": "Invalid rating test"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == "Rating must be between 1 and 5"

def test_create_review_missing_field(reviews_client):
    response = reviews_client.post('/reviews/', json={
        "product_id": 1,
        "rating": 5  # Missing customer_id
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing required field" in data['error']

def test_get_review(reviews_client):
    # Create a review first
    reviews_client.post('/reviews/', json={
        "product_id": 1,
        "customer_id": 2,
        "rating": 5,
        "comment": "Excellent product!"
    })
    response = reviews_client.get('/reviews/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['rating'] == 5
    assert data['comment'] == "Excellent product!"

def test_update_review_valid(reviews_client):
    # Create a review first
    reviews_client.post('/reviews/', json={
        "product_id": 1,
        "customer_id": 2,
        "rating": 5,
        "comment": "Excellent product!"
    })
    response = reviews_client.put('/reviews/1', json={
        "rating": 4,
        "comment": "Updated comment"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "Review updated successfully"
    assert data['review']['rating'] == 4
    assert data['review']['comment'] == "Updated comment"

def test_update_review_invalid_rating(reviews_client):
    # Create a review first
    reviews_client.post('/reviews/', json={
        "product_id": 1,
        "customer_id": 2,
        "rating": 5,
        "comment": "Excellent product!"
    })
    response = reviews_client.put('/reviews/1', json={
        "rating": 10,  # Invalid rating
        "comment": "Updated with invalid rating"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == "Rating must be between 1 and 5"

def test_delete_review(reviews_client):
    # Create a review first
    reviews_client.post('/reviews/', json={
        "product_id": 1,
        "customer_id": 2,
        "rating": 5,
        "comment": "Excellent product!"
    })
    response = reviews_client.delete('/reviews/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "Review deleted successfully"

def test_get_reviews_by_product(reviews_client):
    # Create multiple reviews
    reviews_client.post('/reviews/', json={
        "product_id": 1,
        "customer_id": 2,
        "rating": 5,
        "comment": "Excellent product!"
    })
    reviews_client.post('/reviews/', json={
        "product_id": 1,
        "customer_id": 3,
        "rating": 4,
        "comment": "Very good product!"
    })
    response = reviews_client.get('/reviews/product/1')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2

def test_get_reviews_by_customer(reviews_client):
    # Create multiple reviews by the same customer
    reviews_client.post('/reviews/', json={
        "product_id": 1,
        "customer_id": 2,
        "rating": 5,
        "comment": "Excellent product!"
    })
    reviews_client.post('/reviews/', json={
        "product_id": 2,
        "customer_id": 2,
        "rating": 4,
        "comment": "Good product!"
    })
    response = reviews_client.get('/reviews/customer/2')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
