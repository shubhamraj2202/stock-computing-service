#!/bin/bash

# Base image
FROM --platform=linux/amd64 python:3.9-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get -y --no-install-recommends install \
    gcc \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . .

# Expose the port that the application runs on
EXPOSE 8000

# Start the application
CMD ["python3", "-m", "uvicorn", "stock_computing_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
