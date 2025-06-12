from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from shared.config import Config
from sales.app.db import db  # Ensure absolute imports
import flask_profiler

def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if config:
        app.config.update(config)
        
    print(f"Using database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    db.init_app(app)

    # Register your blueprints
    from .routes import sales_bp
    app.register_blueprint(sales_bp)

    # Flask Profiler Configuration
    app.config["flask_profiler"] = {
        "enabled": True,
        "storage": {
            "engine": "sqlite",
            "FILE": "./flask_profiler.sqlite",  # Save the SQLite file in a persistent volume
        },
        "basicAuth": {
            "enabled": False
        },
    }

    # Initialize Flask Profiler
    flask_profiler.init_app(app)

    return app
