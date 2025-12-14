# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to not create virtual environment in container
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --only main --no-root --no-interaction --no-ansi

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application (shell form to expand $PORT)
CMD uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}
