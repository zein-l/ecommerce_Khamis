# Use Python 3.9 slim base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install netcat for waiting on MySQL readiness
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy inventory code into the container
COPY inventory /app/inventory

# Copy shared utilities into the container
COPY shared /app/shared

# Install dependencies
WORKDIR /app/inventory
COPY inventory/requirements.txt /app/inventory/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH so the app can find shared
ENV PYTHONPATH="/app"

# Expose the service port
EXPOSE 5000

# Wait for MySQL to be ready, then run the app
CMD ["sh", "-c", "while ! nc -z mysql 3306; do echo 'Waiting for MySQL...'; sleep 3; done; python app/run.py"]
