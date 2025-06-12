from datetime import datetime
from sales.app.db import db

class Sale(db.Model):
    """
    Represents a sale record in the database.

    Attributes:
        id (int): Primary key.
        customer_id (int): ID of the customer associated with the sale.
        product_id (int): ID of the product sold.
        quantity (int): Quantity of the product sold.
        total_price (float): Total price of the sale.
        created_at (datetime): Timestamp of when the sale was created.
    """
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Sale {self.id}: Customer {self.customer_id}, Product {self.product_id}, Quantity {self.quantity}, Total Price {self.total_price}>"
