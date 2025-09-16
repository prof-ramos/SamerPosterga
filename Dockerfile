# Multi-arch Dockerfile for Discord RAG Bot
FROM --platform=$BUILDPLATFORM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONHASHSEED=random

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY pyproject.toml .

# Copy knowledge base and embeddings
COPY knowledge/ ./knowledge/
COPY .chroma/ ./.chroma/

# Create non-root user for security
RUN mkdir -p logs && useradd --create-home --shell /bin/bash app     && chown -R app:app /app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Expose port (if needed for web interface)
EXPOSE 8080

# Command to run
CMD ["python", "-m", "src.juridic_bot.main"]