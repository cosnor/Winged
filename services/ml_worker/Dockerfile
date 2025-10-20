# ML Worker Service Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /code

# Copy requirements and install Python dependencies
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application code
COPY ./app /code/app

# Expose FastAPI port
EXPOSE 8003

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
