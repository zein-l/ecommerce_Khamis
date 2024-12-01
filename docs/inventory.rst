Inventory API
=============

.. http:post:: /products
   :synopsis: Create a new product

   **Request Body**

   - `name` (string, required): Name of the product.
   - `description` (string, optional): Description of the product.
   - `price` (float, required): Price of the product.
   - `quantity` (integer, required): Quantity of the product in stock.

   **Response**

   - `201 Created`: Product created successfully.

.. http:get:: /products
   :synopsis: Retrieve all products

   **Response**

   - `200 OK`: List of products.

.. http:get:: /products/<int:product_id>
   :synopsis: Retrieve a single product by ID

   **Response**

   - `200 OK`: Product details.
   - `404 Not Found`: Product not found.

.. http:put:: /products/<int:product_id>
   :synopsis: Update a product

   **Request Body**

   - `name` (string, optional): New name of the product.
   - `description` (string, optional): New description of the product.
   - `price` (float, optional): New price of the product.
   - `quantity` (integer, optional): New quantity of the product.

   **Response**

   - `200 OK`: Product updated successfully.
   - `404 Not Found`: Product not found.

.. http:delete:: /products/<int:product_id>
   :synopsis: Delete a product

   **Response**

   - `200 OK`: Product deleted successfully.
   - `404 Not Found`: Product not found.
