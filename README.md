# 🛒 E-Commerce Microservices Platform

A scalable, modular e-commerce backend system built with Flask, SQLAlchemy, and Docker using a microservices architecture. The platform is divided into four independent services—Customers, Inventory, Sales, and Reviews—each with its own database and RESTful APIs for high scalability, maintainability, and deployment flexibility.

---

## 🎯 Objectives

- ✅ Build a robust e-commerce backend using Flask and SQLAlchemy
- ✅ Enable full user workflows: registration, login, browsing, purchasing, and reviewing
- ✅ Ensure data validation, error handling, and modular service development
- ✅ Containerize services using Docker & integrate with Docker Compose
- ✅ Secure sensitive operations through JWT-based authentication and review moderation

---

## 🏗️ System Architecture

Each service is independent, communicates via REST APIs, and is backed by its own database.

### 1. Customers Service
- Manages user registration, login, and profile updates.
- Key Endpoints: `/register`, `/login`, `/profile/<id>`

### 2. Inventory Service
- Manages product listing, updates, and stock levels.
- Key Endpoints: `/products`, `/products/<id>`, `/products/<id>/update`

### 3. Sales Service
- Handles purchase transactions and payment processing.
- Key Endpoints: `/sales`, `/sales/history/<customer_id>`

### 4. Reviews Service
- Manages customer reviews, moderation, and recommendations.
- Key Endpoints: `/reviews`, `/reviews/<id>`, `/reviews/<id>/moderate`, `/recommendations/<customer_id>`

---

## 🔐 User Authentication & Authorization

- JWT tokens used for authentication.
- Authenticated users required for sensitive actions (e.g., submitting reviews, purchases).
- Review moderation restricted to admin users.

---

## 🧠 Recommendation Engine (Task 9)

A collaborative filtering-based engine suggests products to customers based on their purchase and review history.

- Endpoint: `/recommendations/<customer_id>`
- Recommends similar products based on user preferences.
- Automatically updates with new user activity.

---

## ❤️ Health Check API (Task 4)

Each service includes health endpoints to monitor service availability and readiness:

- `/health/status` – Checks general service health
- `/health/database` – Validates database connectivity

Integrated with Docker Compose for auto-restart and readiness probes.

---

## 🧪 Testing & Validation

- Unit tests for all services using **Pytest**
- Integration tests for end-to-end workflow validation
- All inputs validated and sanitized (e.g., rating 1–5, valid product IDs)
- API tests verified via **Postman**, **cURL**, and automated test suites

---

## 💾 Database Design

- Each microservice has its own schema
- Relationships:  
  - Customers ↔ Sales  
  - Products ↔ Reviews  
  - Reviews ↔ Customers  
- SQLAlchemy models enforce data constraints (`nullable=False`, foreign keys, etc.)

---

## 🔁 Error Handling & Validation

- Database errors handled using `SQLAlchemyException`
- Custom 404/500 responses with meaningful error messages
- Input validation: e.g., rating range checks, missing field detection
- Sanitization applied to prevent SQL injection

---

## 📦 Deployment with Docker

- Each service is containerized with its own Dockerfile
- Docker Compose used for orchestrating services and shared resources
- Health checks ensure services are only live when dependencies are met

---

## 📚 API Documentation

- Each service is fully documented with **Sphinx** and Python **docstrings**
- Postman collection available with:
  - Sample requests/responses
  - Screenshots included in the appendix
- API routes grouped by service and functionality

---

## 🔒 Security Measures (Task 11)

- JWT-based user authentication for secured endpoints
- Admin-only moderation controls for reviews
- Health-check protection to disable unhealthy services
- Input validation and sanitization across all services

---

## 📈 Performance Profiling

- Load tested using **Locust** to simulate high traffic
- Memory profiling via `memory-profiler` to detect performance bottlenecks
- Code coverage analyzed for all test suites

---

## 📂 Repo & Version Control

- Hosted on GitHub: https://github.com/zein-l/Currency-exchange-backend-
- Organized by microservice (each with `Dockerfile`, `requirements.txt`, `README.md`)
- Frequent commits with descriptive messages

---

## 📸 Screenshots & Appendix

- Postman request/response screenshots
- Sample test results from Pytest
- Docker container run screenshots
- API spec examples (JSON format)

---

## ✅ Summary

This project demonstrates a professional-grade e-commerce system using modern best practices in microservices, containerization, API design, and secure architecture. It is well-documented, tested, and ready for further scaling and integration.

---


