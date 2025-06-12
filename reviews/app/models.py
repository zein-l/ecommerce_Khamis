from sqlalchemy.sql import func
from reviews.app.db import db

class Review(db.Model):
    """
    Represents a product review submitted by a customer.

    This class defines the structure and functionality for storing and managing product reviews.
    Reviews allow customers to rate and comment on products they have used.

    **Attributes:**
    - `id` (int): Primary key for the review.
    - `product_id` (int): ID of the product being reviewed.
    - `customer_id` (int): ID of the customer who submitted the review.
    - `rating` (int): Rating given by the customer (1-5).
    - `comment` (str): Optional textual feedback from the customer.
    - `created_at` (datetime): Timestamp when the review was created.
    - `updated_at` (datetime): Timestamp when the review was last updated.

    **Methods:**
    - `to_dict()`: Converts the review instance into a dictionary format.
    """

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, nullable=False, comment="Foreign key linking to the product being reviewed.")
    customer_id = db.Column(db.Integer, nullable=False, comment="Foreign key linking to the customer who submitted the review.")
    rating = db.Column(db.Integer, nullable=False, comment="Customer's rating of the product (1-5).")
    comment = db.Column(db.Text, nullable=True, comment="Optional customer feedback about the product.")
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), comment="Timestamp of review creation.")
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now(), comment="Timestamp of last review update.")

    def __repr__(self):
        """
        Provides a string representation of the Review instance.

        **Returns:**
        - str: A formatted string containing review details, useful for debugging.
        """
        return (
            f"<Review id={self.id} product_id={self.product_id} "
            f"customer_id={self.customer_id} rating={self.rating}>"
        )

    def to_dict(self):
        """
        Converts the Review instance into a dictionary format for serialization.

        **Returns:**
        - dict: A dictionary containing all relevant details of the review.
        """
        return {
            "id": self.id,
            "product_id": self.product_id,
            "customer_id": self.customer_id,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
