Project Overview
This project implements a scalable and modular e-commerce system using a microservices architecture. The system consists of four main services: Customers, Inventory, Sales, and Reviews. Each service has been developed independently, with its own database and RESTful APIs, ensuring modularity and scalability.

Objectives
•	To create a robust e-commerce platform using Flask and SQLAlchemy.
•	To enable customers to register, interact with products, submit reviews, and purchase items.
•	To provide comprehensive API functionality, error handling, and data validation.
•	To deploy the application using Docker for consistency across environments.
•	To implement user authentication and moderation for sensitive actions like reviews.
________________________________________
4. System Architecture
Service Descriptions
1.	Customers Service:
Manages user registration, login, and profile information.
APIs include registering customers, fetching customer details, and updating profiles.
2.	Inventory Service:
Handles product management, including adding, updating, and deleting products.
APIs include fetching all products, retrieving details of specific products, and managing stock.
3.	Sales Service:
Processes customer purchases and maintains sales history.
APIs include creating sales transactions, retrieving sales history, and managing payments.
4.	Reviews Service:
Allows customers to submit feedback on purchased products.
APIs include submitting, updating, deleting, and moderating reviews.
________________________________________
5. Implementation Details
Service-Specific Implementation
1.	Customers:
o	Key APIs: Customer registration, profile update, and login.
o	Challenges: Ensuring secure password storage and handling edge cases in registration.
2.	Inventory:
o	Key APIs: Adding products, updating product information, fetching product lists.
o	Challenges: Managing stock levels dynamically with purchases.
3.	Sales:
o	Key APIs: Creating a sale, retrieving transaction history.
o	Challenges: Ensuring transactional integrity with inventory updates.
4.	Reviews:
o	Key APIs: Submitting reviews, updating and deleting reviews, retrieving reviews by product/customer.
o	Challenges: Implementing user validation and review moderation.
API Documentation
•	Each service’s APIs were documented with Sphinx and Docstrings, and tested using Postman , cURL , and test cases.
•	Sample requests and responses were saved in a Postman collection for easy testing.
•	Screenshots of Postman requests and responses are included in the appendix.
________________________________________
6. Database Design
Schema Diagram
A schema diagram was created for all services, detailing relationships such as products linked to reviews, customers linked to sales, etc.
________________________________________
7. Error Handling and Validation
Error Management:
•	SQLAlchemyException: Handled errors related to database operations, ensuring the application remained responsive.
•	404 Errors: Provided clear error messages for invalid resource access.
Validation:
•	Input Validation: Applied validation for fields like ratings in reviews (1–5).
•	Sanitization: All inputs were sanitized to prevent SQL injection and ensure secure database operations.
________________________________________
8. Testing
Testing Strategy:
•	Unit tests were written using Pytest for each service.
•	Integration tests ensured smooth inter-service communication.
Test Cases:
•	Test cases were created for all major functionalities, such as creating a review, updating customer profiles, and handling purchases.
•	Pytest results confirmed that all test cases passed successfully.
________________________________________
9. Deployment and Integration
Docker Setup:
•	Each service was containerized using a Dockerfile.
•	Docker Compose was used to integrate all services and their respective dependencies.
________________________________________
10. Documentation and Profiling
Documentation:
•	Documentation was generated using Sphinx for all services.
•	Detailed explanations for routes, models, and methods were included.
Performance Profiling:
•	Memory and performance profiling were performed using tools like memory-profiler and Locust for load testing, ensuring scalability under heavy usage.
•	Code coverage was analyzed using coverage tools to ensure test completeness.
________________________________________
11. GitHub and Version Control
Repository:
•	The project code was pushed to a GitHub repository.
•	Regular commits were made, documenting progress and addressing issues.
________________________________________
12. Docker and Images
Each service, including dependencies, was packaged into a container using Dockerfiles. Screenshots of running containers are included in the appendix.
________________________________________
13. Validation and Sanitization
•	Input fields for the Reviews service were validated to ensure proper data types and prevent SQL injection.
•	Invalid ratings, missing fields, and incorrect data types were handled gracefully.
________________________________________
14. User Authentication
•	Authentication was implemented using JWT tokens for secured API access.
•	Only authenticated users could perform sensitive actions like creating or modifying reviews.
________________________________________
15. Moderation
•	Moderation APIs were included to allow administrators to approve or flag inappropriate reviews.
•	Flagging functionality ensures a clean review system.
________________________________________
16. Additional Professional Tasks
Task 4: Health Checks: Add health-check APIs for all services to monitor their availability and performance.
Steps Implemented:
1.	Database Connectivity Check:
o	Created an endpoint /health/database to validate the connection to the reviews database.
2.	Application Status Check:
o	Created an endpoint /health/status to check the service's overall health, including key dependencies.
3.	Integration with Docker:
o	Integrated health checks in the Docker configuration to ensure the service only runs when it is fully operational.
4.	Error Handling:
o	Implemented comprehensive error handling for unexpected scenarios to prevent service downtime.
Task 9: Recommendation System: Add a recommendation engine for customers, suggesting products based on purchase history (e.g., using collaborative filtering or simple rules).
Steps Implemented:
1.	Data Preparation: Utilized product ratings and customer feedback from the reviews database.
2.	Algorithm Implementation: Implemented a collaborative filtering approach to suggest products based on customer reviews and ratings.
3.	API Endpoint:
o	Created an endpoint /recommendations/<customer_id> to fetch recommended products for a specific customer.
4.	Real-time Update: Ensured the recommendations adapt dynamically based on new reviews or changes in customer preferences.
Task 11: Security measures:
Steps Implemented:
1.	Input Validation: Validated and sanitized all user inputs to prevent SQL injection and XSS attacks.
2.	Authentication and Authorization: Integrated JWT-based authentication to ensure only authorized users can submit or modify reviews.
3.	Moderation Tools: Added a moderation feature for administrators to flag and approve reviews for content violations.
