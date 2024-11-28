from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from shared.config import Config
from customers.app.db import db
import flask_profiler

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) 
    db.init_app(app)

    # Register your blueprints
    from .routes import customers_bp
    app.register_blueprint(customers_bp)

    # Flask Profiler Configuration
    app.config["flask_profiler"] = {
        "enabled": True,
        "storage": {
            "engine": "sqlite",
            "FILE": "./flask_profiler.sqlite",   # Save the SQLite file in a persistent volume
        },
        "basicAuth": {
            "enabled": False
        },
        
    }

    # Initialize Flask Profiler
    flask_profiler.init_app(app)

    return app
