# Use official Python base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install PostgreSQL client
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && apt-get -y install --no-install-recommends postgresql-client

# Copy requirements.txt first for caching dependencies
COPY ../requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app code
COPY . .

# Default command to run your app
CMD ["python", "main.py"]
