from customers.app.db import db  # Import `db` from db.py




class Customer(db.Model):
    __tablename__ = 'customers'
    __table_args__ = {'extend_existing': True}  # Avoid redefinition errors

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(10))
    marital_status = db.Column(db.String(10))
    wallet_balance = db.Column(db.Float, default=0.0)
    role = db.Column(db.String(20), default='customer')

    def __repr__(self):
        return f"<Customer {self.username}>"
