# Use Python 3.9 slim base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install netcat-openbsd for checking database readiness
RUN apt-get update && apt-get install -y netcat-openbsd sqlite3

# Copy requirements file into the container
COPY customers/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the `customers` and `shared` directories into the container
COPY customers /app/customers
COPY shared /app/shared



# Set the working directory for running the app
WORKDIR /app/customers/app

# Add `/app` to the PYTHONPATH to include `shared/`
ENV PYTHONPATH="/app"

# Expose the application's port
EXPOSE 5000

# Command to wait for MySQL and then run the application
CMD ["sh", "-c", "while ! nc -z mysql 3306; do echo 'Waiting for MySQL...'; sleep
