# Backend Dockerfile
# Build context is the project root (set in docker-compose.yml)
FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code (preserving package structure)
COPY backend/ ./backend/
COPY .env* ./

# Expose port
EXPOSE 8000

# Run uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
