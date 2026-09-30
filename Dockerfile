# ================================
# App Builder OS
# ================================
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir \
    --only-binary :all: \
    --prefix=/install \
    -r requirements.txt


# ================================
# App Runtime OS
# ================================
FROM python:3.12-slim AS runtime

WORKDIR /app

RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd appuser

# Copy dependencies from builder
COPY --from=builder \
    --chown=appuser:appuser \
    /install /usr/local

# Copy specific application files and folders safely
COPY app.py .
COPY static/ ./static/
COPY templates/ ./templates/

EXPOSE 8080

USER appuser

# Pass App Version at build time
ARG APP_VERSION=v1.0.0
ENV APP_VERSION=${APP_VERSION}

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]