import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    DB_HOST = os.getenv('DB_HOST', 'mysql')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'ecommerce_db')
    DB_USER = os.getenv('DB_USER', 'ecommerce_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'securepassword')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
