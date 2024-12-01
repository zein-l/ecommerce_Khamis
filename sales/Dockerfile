# Use Python 3.9 slim base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install netcat for waiting on MySQL readiness
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy sales code into the container
COPY sales /app/sales

# Install dependencies
WORKDIR /app/sales
COPY sales/requirements.txt /app/sales/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH so the app can find shared
ENV PYTHONPATH="/app"

# Expose the service port
EXPOSE 5003

# Wait for MySQL to be ready, then run the app
CMD ["sh", "-c", "while ! nc -z mysql 3306; do echo 'Waiting for MySQL...'; sleep 3; done; python app/run.py"]
