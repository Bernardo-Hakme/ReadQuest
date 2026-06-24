# 1. Use an official lightweight Python image as the base operating system
FROM python:3.11-slim

# 2. Set environment variables to optimize Python inside Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the virtual container
WORKDIR /app

# 4. Install system dependencies needed for PostgreSQL and compiling binary tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy the requirements file from your laptop into the container
COPY requirements.txt /app/

# 6. Install all Python packages directly inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy the rest of your local Django project code into the container
COPY . /app/