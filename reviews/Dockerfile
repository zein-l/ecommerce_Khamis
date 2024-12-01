# Use Python 3.9 slim base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy Reviews service code into the container
COPY reviews /app/reviews

# Copy shared utilities into the container
COPY shared /app/shared

# Install Python dependencies
WORKDIR /app/reviews
COPY reviews/requirements.txt /app/reviews/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH so the app can find shared modules
ENV PYTHONPATH="/app"

# Expose the Reviews service port
EXPOSE 5004

# Wait for the database to be ready, then run the app
CMD ["sh", "-c", "while ! nc -z mysql 3306; do echo 'Waiting for MySQL...'; sleep 3; done; python app/run.py"]
