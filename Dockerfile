# Multi-stage build for optimized image size
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Install git (required for git dependencies)
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Create virtual environment and install dependencies
RUN uv venv /opt/venv && \
    uv pip install --python /opt/venv/bin/python --no-cache -r pyproject.toml

# Production stage
FROM python:3.12-slim-bookworm

# Install system dependencies if needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 onkyo && \
    mkdir -p /app && \
    chown -R onkyo:onkyo /app

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY --chown=onkyo:onkyo . .

# Use non-root user
USER onkyo

# Activate virtual environment
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["python", "-u", "main.py"]