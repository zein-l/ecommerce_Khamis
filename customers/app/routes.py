from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from .models import db, Customer
from .validators import CustomerSchema
from .auth import token_required
from marshmallow import ValidationError
from memory_profiler import profile

customers_bp = Blueprint('customers_bp', __name__)

@customers_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for the customers service.
    
    Returns:
        - 200: Indicates that the service is up and running.
    """
    return jsonify({"status": "UP", "message": "Customers service is healthy"}), 200

@customers_bp.route('/customers/register', methods=['POST'])
def register_customer():
    """
    Registers a new customer.
    """
    data = request.get_json()
    schema = CustomerSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Invalid input data.", "details": err.messages}), 400

    if Customer.query.filter_by(username=validated_data['username']).first():
        return jsonify({"error": f"Username '{validated_data['username']}' is already taken."}), 400

    hashed_password = generate_password_hash(validated_data['password'])
    new_customer = Customer(
        full_name=validated_data['full_name'],
        username=validated_data['username'],
        password_hash=hashed_password,
        age=validated_data['age'],
        address=validated_data['address'],
        gender=validated_data.get('gender'),
        marital_status=validated_data.get('marital_status')
    )

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"message": "Customer registered successfully.", "customer_id": new_customer.id}), 201


@customers_bp.route('/customers/<username>', methods=['DELETE'])
def delete_customer(username):
    """
    Deletes a customer by their username.
    """
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({"error": f"Customer with username '{username}' not found."}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": f"Customer '{username}' deleted successfully."}), 200


@customers_bp.route('/customers/<username>', methods=['PUT'])
def update_customer(username):
    """
    Updates customer information.
    """
    data = request.get_json()
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({"error": f"Customer with username '{username}' not found."}), 404

    if 'full_name' in data:
        customer.full_name = data['full_name']
    if 'password' in data:
        customer.password_hash = generate_password_hash(data['password'])
    if 'age' in data:
        customer.age = data['age']
    if 'address' in data:
        customer.address = data['address']
    if 'gender' in data:
        customer.gender = data['gender']
    if 'marital_status' in data:
        customer.marital_status = data['marital_status']

    db.session.commit()
    return jsonify({"message": f"Customer '{username}' updated successfully."}), 200


@customers_bp.route('/customers/<username>', methods=['GET'])
def get_customer_by_username(username):
    """
    Retrieves a customer's details by username.
    """
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    result = {
        "id": customer.id,
        "full_name": customer.full_name,
        "username": customer.username,
        "age": customer.age,
        "address": customer.address,
        "gender": customer.gender,
        "marital_status": customer.marital_status,
        "wallet_balance": customer.wallet_balance,
        "role": customer.role,
    }
    return jsonify(result), 200


@customers_bp.route('/customers', methods=['GET'])
def get_all_customers():
    """
    Retrieves all customers from the database.
    """
    customers = Customer.query.all()
    result = [
        {
            "id": customer.id,
            "full_name": customer.full_name,
            "username": customer.username,
            "age": customer.age,
            "address": customer.address,
            "gender": customer.gender,
            "marital_status": customer.marital_status,
            "wallet_balance": customer.wallet_balance,
            "role": customer.role,
        }
        for customer in customers
    ]
    return jsonify(result), 200


@customers_bp.route('/customers/<string:username>/charge', methods=['POST'])
def charge_wallet(username):
    """
    Charges a customer's wallet with a specified amount.
    """
    data = request.get_json()
    amount = data.get("amount")

    if not amount or amount <= 0:
        return jsonify({"error": "Amount must be a positive value."}), 400

    customer = Customer.query.filter_by(username=username).first()

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    customer.wallet_balance += amount
    db.session.commit()

    return jsonify({
        "message": "Wallet charged successfully.",
        "new_balance": customer.wallet_balance
    }), 200


@customers_bp.route('/customers/<string:username>/deduct', methods=['POST'])
def deduct_wallet(username):
    """
    Deducts a specified amount from a customer's wallet.
    """
    data = request.get_json()
    amount = data.get("amount")

    if not amount or amount <= 0:
        return jsonify({"error": "Amount must be a positive value."}), 400

    customer = Customer.query.filter_by(username=username).first()

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    if customer.wallet_balance < amount:
        return jsonify({"error": "Insufficient wallet balance."}), 400

    customer.wallet_balance -= amount
    db.session.commit()

    return jsonify({
        "message": "Wallet deducted successfully.",
        "new_balance": customer.wallet_balance
    }), 200
