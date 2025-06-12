# Use a lightweight Python image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port your Flask app runs on
EXPOSE 5001

# Command to start the Flask app
CMD ["python", "app.py"]
