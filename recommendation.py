from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Flask App and Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recommendation.db'  # Example SQLite DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Review(db.Model):
    """
    Represents a product review submitted by a customer.
    """
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "customer_id": self.customer_id,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

class Product(db.Model):
    """
    Represents a product in the e-commerce platform.
    """
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
        }

# Recommendation Logic
def get_product_recommendations(customer_id, top_n=5):
    """
    Generate product recommendations for a customer based on review ratings.

    Args:
    - customer_id (int): The ID of the customer.
    - top_n (int): The number of recommendations to return.

    Returns:
    - list: A list of recommended products with their scores.
    """
    # Fetch all reviews
    reviews = Review.query.all()

    if not reviews:
        return []

    # Prepare data for collaborative filtering
    customers = list(set([review.customer_id for review in reviews]))
    products = list(set([review.product_id for review in reviews]))

    customer_idx = {customer: idx for idx, customer in enumerate(customers)}
    product_idx = {product: idx for idx, product in enumerate(products)}

    # Build rating matrix
    rating_matrix = np.zeros((len(customers), len(products)))
    for review in reviews:
        rating_matrix[customer_idx[review.customer_id], product_idx[review.product_id]] = review.rating

    # Compute cosine similarity
    similarity_matrix = cosine_similarity(rating_matrix)

    # Find the customer's index
    target_idx = customer_idx.get(customer_id)
    if target_idx is None:
        return []

    # Compute recommendations
    scores = np.dot(similarity_matrix[target_idx], rating_matrix)
    recommended_indices = np.argsort(-scores)

    recommended_products = []
    for idx in recommended_indices[:top_n]:
        for product, product_idx_val in product_idx.items():
            if product_idx_val == idx and scores[idx] > 0:
                recommended_products.append({
                    "product_id": product,
                    "score": scores[idx]
                })

    return recommended_products

# Routes
@app.route('/recommendations/<int:customer_id>', methods=['GET'])
def recommend(customer_id):
    """
    API endpoint to get product recommendations for a customer.
    """
    top_n = request.args.get('top_n', default=5, type=int)
    recommendations = get_product_recommendations(customer_id, top_n=top_n)

    # Fetch product details
    products = []
    for recommendation in recommendations:
        product = Product.query.get(recommendation['product_id'])
        if product:
            products.append({
                "product": product.to_dict(),
                "score": recommendation['score']
            })

    return jsonify({
        "customer_id": customer_id,
        "recommendations": products
    }), 200

# Initialize and Run
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure all tables are created
    app.run(debug=True, host='0.0.0.0', port=5005)
