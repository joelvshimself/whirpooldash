# syntax=docker/dockerfile:1.6
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Create app directory
WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt /app/requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# Copy source code
COPY . /app

# Create non-root user and set permissions
RUN groupadd -r appgroup && useradd -m -r -g appgroup appuser && \
    chown -R appuser:appgroup /app && \
    chmod +x /app/entrypoint.sh

# Expose port 8080 for Azure App Service
EXPOSE 8080

# Run as non-root user for security
USER appuser

# Start Streamlit via entrypoint script
CMD ["/app/entrypoint.sh"]


