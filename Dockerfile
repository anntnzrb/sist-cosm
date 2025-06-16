FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install UV
RUN pip install uv

# Copy and install dependencies
COPY pyproject.toml uv.lock README.md ./
RUN uv sync

# Copy project
COPY . .

# Run the application
CMD ["sh", "-c", "sleep 10 && uv run python manage.py migrate && uv run python manage.py runserver 0.0.0.0:8000"]