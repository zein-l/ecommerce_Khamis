from customers.app.app import app 

@app.route('/customers/register', methods=['POST'])
def register_customer():
    """
    Register a new customer.

    **Endpoint**: `POST /customers/register`

    **Request Body**:
    - `full_name` (str): Full name of the customer.
    - `username` (str): Unique username.
    - `password` (str): Account password.
    - `age` (int): Age of the customer.
    - `address` (str): Address of the customer.
    - `gender` (str, optional): Gender of the customer.
    - `marital_status` (str, optional): Marital status.

    **Responses**:
    - `201 Created`: Customer registered successfully.
    - `400 Bad Request`: Validation errors or username already taken.
    """
    # Implementation
