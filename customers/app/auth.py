import jwt 
from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps
from customers.app.models import Customer
from shared.config import Config

def generate_token(customer_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow(),
        'sub': customer_id
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing.'}), 401
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            current_user = Customer.query.get(data['sub'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token.'}), 401
        return f(current_user, *args, **kwargs)
    return decorated
