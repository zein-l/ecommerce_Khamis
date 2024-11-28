import pytest
from customers.app import create_app
from customers.app.db import db
import sys
import os

# Add project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()  # Clear any leftover data
            db.create_all()  # Set up fresh schema
        yield client
        db.session.remove()  # Cleanup after test
