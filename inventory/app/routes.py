from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from .db import db
from .models import Product

# Blueprint for inventory service
inventory_bp = Blueprint('inventory', __name__)

# Health Check Endpoint
@inventory_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the service is up and running.
    
    Returns:
        Response: JSON object indicating the health status of the service.
    """
    try:
        # Perform a simple query to verify database connectivity
        db.session.execute("SELECT 1")
        return jsonify({'status': 'healthy'}), 200
    except SQLAlchemyError as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500


@inventory_bp.route('/products', methods=['POST'])
def create_product():
    """
    Create a new product.

    Request JSON:
        - name (str): The name of the product.
        - description (str, optional): A description of the product.
        - price (float): The price of the product.
        - quantity (int): The quantity of the product in stock.

    Returns:
        Response: JSON object containing a success message and the created product's ID.
    """
    data = request.json
    product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        quantity=data['quantity']
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully', 'product': product.id}), 201

@inventory_bp.route('/products', methods=['GET'])
def get_products():
    """
    Retrieve all products.

    Returns:
        Response: JSON list of all products, where each product contains:
            - id (int): The product ID.
            - name (str): The name of the product.
            - description (str): The description of the product.
            - price (float): The price of the product.
            - quantity (int): The quantity of the product in stock.
    """
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'quantity': p.quantity
    } for p in products])

@inventory_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Retrieve a single product by its ID.

    Args:
        product_id (int): The ID of the product to retrieve.

    Returns:
        Response: JSON object containing product details:
            - id (int): The product ID.
            - name (str): The name of the product.
            - description (str): The description of the product.
            - price (float): The price of the product.
            - quantity (int): The quantity of the product in stock.

    Raises:
        404: If the product with the given ID is not found.
    """
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'quantity': product.quantity
    })

@inventory_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """
    Update an existing product by its ID.

    Args:
        product_id (int): The ID of the product to update.

    Request JSON:
        - name (str, optional): The new name of the product.
        - description (str, optional): The new description of the product.
        - price (float, optional): The new price of the product.
        - quantity (int, optional): The new quantity of the product in stock.

    Returns:
        Response: JSON object containing a success message.

    Raises:
        404: If the product with the given ID is not found.
    """
    product = Product.query.get_or_404(product_id)
    data = request.json
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.quantity = data.get('quantity', product.quantity)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@inventory_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    Delete a product by its ID.

    Args:
        product_id (int): The ID of the product to delete.

    Returns:
        Response: JSON object containing a success message.

    Raises:
        404: If the product with the given ID is not found.
    """
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})
