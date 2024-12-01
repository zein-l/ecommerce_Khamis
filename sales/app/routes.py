from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from sales.app.db import db
from .models import Sale  # Replace with your actual model for sales

# Create a Blueprint for the sales service
sales_bp = Blueprint('sales_bp', __name__)

@sales_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health Check API.

    Returns:
        Response: JSON object indicating the health status of the service.
    """
    try:
        # Perform a simple database query to verify connectivity
        db.session.execute('SELECT 1')
        return jsonify({"status": "healthy"}), 200
    except SQLAlchemyError as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@sales_bp.route('/sales', methods=['POST'])
def create_sale():
    """
    Create a new sale record.

    Request JSON:
        - customer_id (int): ID of the customer.
        - product_id (int): ID of the product.
        - quantity (int): Quantity of the product sold.
        - total_price (float): Total price of the sale.

    Returns:
        Response: JSON object containing a success message and the created sale's ID.
    """
    data = request.json

    # Validate the input data
    if not all(key in data for key in ("customer_id", "product_id", "quantity", "total_price")):
        return jsonify({"error": "Missing required fields"}), 400

    # Create a new sale object
    sale = Sale(
        customer_id=data['customer_id'],
        product_id=data['product_id'],
        quantity=data['quantity'],
        total_price=data['total_price']
    )

    # Add the sale to the database
    db.session.add(sale)
    db.session.commit()

    return jsonify({"message": "Sale created successfully", "sale_id": sale.id}), 201


@sales_bp.route('/sales', methods=['GET'])
def get_sales():
    """
    Retrieve all sales records.

    Returns:
        Response: JSON list of all sales, where each sale contains:
            - id (int): The sale ID.
            - customer_id (int): ID of the customer.
            - product_id (int): ID of the product.
            - quantity (int): Quantity of the product sold.
            - total_price (float): Total price of the sale.
    """
    sales = Sale.query.all()
    return jsonify([{
        'id': sale.id,
        'customer_id': sale.customer_id,
        'product_id': sale.product_id,
        'quantity': sale.quantity,
        'total_price': sale.total_price
    } for sale in sales])


@sales_bp.route('/sales/<int:sale_id>', methods=['GET'])
def get_sale(sale_id):
    """
    Retrieve a single sale by its ID.

    Args:
        sale_id (int): The ID of the sale to retrieve.

    Returns:
        Response: JSON object containing sale details.

    Raises:
        404: If the sale with the given ID is not found.
    """
    sale = Sale.query.get_or_404(sale_id)
    return jsonify({
        'id': sale.id,
        'customer_id': sale.customer_id,
        'product_id': sale.product_id,
        'quantity': sale.quantity,
        'total_price': sale.total_price
    })


@sales_bp.route('/sales/<int:sale_id>', methods=['PUT'])
def update_sale(sale_id):
    """
    Update an existing sale by its ID.

    Args:
        sale_id (int): The ID of the sale to update.

    Request JSON:
        - Any of the fields to update (e.g., customer_id, product_id, quantity, total_price).

    Returns:
        Response: JSON object containing a success message.

    Raises:
        404: If the sale with the given ID is not found.
    """
    sale = Sale.query.get_or_404(sale_id)
    data = request.json

    if 'customer_id' in data:
        sale.customer_id = data['customer_id']
    if 'product_id' in data:
        sale.product_id = data['product_id']
    if 'quantity' in data:
        sale.quantity = data['quantity']
    if 'total_price' in data:
        sale.total_price = data['total_price']

    db.session.commit()
    return jsonify({"message": "Sale updated successfully"})


@sales_bp.route('/sales/<int:sale_id>', methods=['DELETE'])
def delete_sale(sale_id):
    """
    Delete a sale by its ID.

    Args:
        sale_id (int): The ID of the sale to delete.

    Returns:
        Response: JSON object containing a success message.

    Raises:
        404: If the sale with the given ID is not found.
    """
    sale = Sale.query.get_or_404(sale_id)
    db.session.delete(sale)
    db.session.commit()
    return jsonify({"message": "Sale deleted successfully"})
