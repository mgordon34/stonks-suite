FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY data-service/requirements.txt /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY data-service/src/ /app/src/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import pika; print('Data service is healthy')" || exit 1

EXPOSE 8001
CMD ["python", "-m", "uvicorn", "--app-dir", "./src", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
