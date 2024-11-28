Customers Service Documentation
===============================

This section documents the API endpoints, models, and workflows for the `customers` service.

Overview
--------

The `customers` service is responsible for handling customer registration, updates, deletion, wallet operations, and retrieval of customer data.

Endpoints
---------

**Base URL:** `/customers`

1. **Register Customer**
   - **Method:** POST
   - **URL:** `/customers/register`
   - **Description:** Register a new customer.
   - **Request Body:**
     - `full_name` (str): Customer's full name.
     - `username` (str): Unique username.
     - `password` (str): Plaintext password.
     - `age` (int): Age of the customer.
     - `address` (str): Customer's address.
     - `gender` (str, optional): Customer's gender.
     - `marital_status` (str, optional): Marital status.

2. **Delete Customer**
   - **Method:** DELETE
   - **URL:** `/customers/<username>`
   - **Description:** Delete a customer by username.

3. **Update Customer**
   - **Method:** PUT
   - **URL:** `/customers/<username>`
   - **Description:** Update details of a customer by username.

4. **Get All Customers**
   - **Method:** GET
   - **URL:** `/customers`
   - **Description:** Retrieve a list of all registered customers.

5. **Get Customer by Username**
   - **Method:** GET
   - **URL:** `/customers/<username>`
   - **Description:** Retrieve detailed information about a specific customer.

6. **Charge Wallet**
   - **Method:** POST
   - **URL:** `/customers/<username>/charge`
   - **Description:** Add money to a customer's wallet.

7. **Deduct Wallet**
   - **Method:** POST
   - **URL:** `/customers/<username>/deduct`
   - **Description:** Deduct money from a customer's wallet.

---

Once the other services are created (Inventory, Sales, Reviews), you can expand the documentation in a similar way.

### Next Steps:
1. Run `make html` in your Sphinx directory to generate the documentation:
   ```bash
   make html
