# Stage 1: Install dependencies into a separate layer
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Copy only the installed packages and app code
FROM python:3.12-slim

# Create a non-root user for security
RUN useradd -r -s /bin/false appuser
WORKDIR /app

COPY --from=builder /install /usr/local
COPY . .

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# Health check for Docker and Kubernetes to verify the app is running
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/healthz')" || exit 1

CMD ["python", "app.py"]