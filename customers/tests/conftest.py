import pytest
from customers.app import app as flask_app

@pytest.fixture
def app():
    """
    Returns the Flask application instance for testing.
    """
    yield flask_app
