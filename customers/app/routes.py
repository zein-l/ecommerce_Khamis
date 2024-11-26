from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from .models import db, Customer
from .validators import CustomerSchema
from .auth import token_required
from marshmallow import ValidationError
from customers.app.db import db 
from customers.app.models import Customer




customers_bp = Blueprint('customers_bp', __name__)

@customers_bp.route('/customers/register', methods=['POST'])
def register_customer():
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
    
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({"error": f"Customer with username '{username}' not found."}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": f"Customer '{username}' deleted successfully."}), 200
  