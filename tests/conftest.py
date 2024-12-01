import pytest
from inventory.app import create_app as create_inventory_app
from customers.app import create_app as create_customers_app
from inventory.app.db import db as inventory_db
from customers.app.db import db as customers_db
import os
import sys


@pytest.fixture
def inventory_client():
    app = create_inventory_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # Use SQLite
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    with app.test_client() as client:
        with app.app_context():
            inventory_db.create_all()  # Create tables for SQLite
        yield client
        with app.app_context():
            inventory_db.session.remove()
            inventory_db.get_engine().dispose()

@pytest.fixture
def customers_client():
    app = create_customers_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',  # Use SQLite
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    with app.test_client() as client:
        with app.app_context():
            customers_db.create_all()  # Create tables for SQLite
        yield client
        with app.app_context():
            customers_db.session.remove()
            customers_db.get_engine().dispose()
