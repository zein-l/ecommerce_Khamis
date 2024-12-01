from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from reviews.app.db import db
from reviews.app.models import Review
from reviews.app.schemas import ReviewSchema
from marshmallow.exceptions import ValidationError

# Define blueprint
reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

# Initialize schema
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)  # For lists of reviews


@reviews_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for the Reviews service.

    **GET /reviews/health**

    **Returns:**
    - 200: Service is healthy.
    """
    try:
        # Perform a simple database query to verify connectivity
        db.session.execute('SELECT 1')
        return jsonify({"status": "healthy"}), 200
    except SQLAlchemyError:
        return jsonify({"status": "unhealthy", "error": "Database connection failed"}), 500


@reviews_bp.route('/', methods=['POST'])
def create_review():
    """
    Create a new review for a product.

    **POST /reviews/**

    JSON Payload:
    ```json
    {
        "product_id": int,
        "customer_id": int,
        "rating": int,
        "comment": str
    }
    ```

    **Returns:**
    - 201: Review created successfully.
    - 400: Validation error or missing fields.
    - 500: Database error.
    """
    try:
        # Validate and sanitize input
        data = review_schema.load(request.get_json())
        review = Review(
            product_id=data["product_id"],
            customer_id=data["customer_id"],
            rating=data["rating"],
            comment=data.get("comment")
        )
        db.session.add(review)
        db.session.commit()
        return jsonify({"message": "Review created successfully", "review": review.to_dict()}), 201
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


@reviews_bp.route('/<int:review_id>', methods=['GET'])
def get_review(review_id):
    """
    Retrieve details of a specific review.

    **GET /reviews/<review_id>**

    **Parameters:**
    - `review_id` (int): ID of the review to retrieve.

    **Returns:**
    - 200: Review data.
    - 404: Review not found.
    """
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    return jsonify(review.to_dict()), 200


@reviews_bp.route('/product/<int:product_id>', methods=['GET'])
def get_reviews_by_product(product_id):
    """
    Retrieve all reviews for a specific product.

    **GET /reviews/product/<product_id>**

    **Parameters:**
    - `product_id` (int): ID of the product.

    **Returns:**
    - 200: List of reviews.
    """
    reviews = Review.query.filter_by(product_id=product_id).all()
    return jsonify(reviews_schema.dump(reviews)), 200


@reviews_bp.route('/customer/<int:customer_id>', methods=['GET'])
def get_reviews_by_customer(customer_id):
    """
    Retrieve all reviews submitted by a specific customer.

    **GET /reviews/customer/<customer_id>**

    **Parameters:**
    - `customer_id` (int): ID of the customer.

    **Returns:**
    - 200: List of reviews.
    """
    reviews = Review.query.filter_by(customer_id=customer_id).all()
    return jsonify(reviews_schema.dump(reviews)), 200


@reviews_bp.route('/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Update an existing review.

    **PUT /reviews/<review_id>**

    JSON Payload:
    ```json
    {
        "rating": int,
        "comment": str
    }
    ```

    **Parameters:**
    - `review_id` (int): ID of the review to update.

    **Returns:**
    - 200: Review updated successfully.
    - 400: Validation error or missing fields.
    - 404: Review not found.
    - 500: Database error.
    """
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    try:
        # Validate and sanitize input
        data = review_schema.load(request.get_json(), partial=True)
        if "rating" in data:
            review.rating = data["rating"]
        if "comment" in data:
            review.comment = data["comment"]
        db.session.commit()
        return jsonify({"message": "Review updated successfully", "review": review.to_dict()}), 200
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Delete a specific review.

    **DELETE /reviews/<review_id>**

    **Parameters:**
    - `review_id` (int): ID of the review to delete.

    **Returns:**
    - 200: Review deleted successfully.
    - 404: Review not found.
    - 500: Database error.
    """
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    try:
        db.session.delete(review)
        db.session.commit()
        return jsonify({"message": "Review deleted successfully"}), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500


@reviews_bp.route('/moderate/<int:review_id>', methods=['POST'])
def moderate_review(review_id):
    """
    Moderate a review by flagging or approving it.

    **POST /reviews/moderate/<review_id>**

    JSON Payload:
    ```json
    {
        "action": "approve" or "flag"
    }
    ```

    **Parameters:**
    - `review_id` (int): ID of the review to moderate.

    **Returns:**
    - 200: Review moderated successfully.
    - 400: Invalid action.
    - 404: Review not found.
    """
    data = request.get_json()
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    action = data.get("action")
    if action not in ["approve", "flag"]:
        return jsonify({"error": "Invalid action. Must be 'approve' or 'flag'"}), 400

    # Placeholder for moderation logic
    return jsonify({"message": f"Review {action}d successfully", "review": review.to_dict()}), 200
