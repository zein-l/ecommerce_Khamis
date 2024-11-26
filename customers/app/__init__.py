from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from shared.config import Config
from customers.app.db import db



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) 
    db.init_app(app)

    from .routes import customers_bp
    app.register_blueprint(customers_bp)

    return app
