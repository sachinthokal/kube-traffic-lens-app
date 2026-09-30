# ================================
# App Builder OS
# ================================
FROM python:3.12-alpine3.24 AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir \
    --only-binary :all: \
    --prefix=/install \
    -r requirements.txt


# ================================
# App Runtime OS
# ================================
FROM python:3.12-alpine3.24 AS runtime

WORKDIR /app

# Upgrade Alpine OS packages
RUN apk upgrade --no-cache

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN adduser -D -s /sbin/nologin appuser

# Copy dependencies from builder
COPY --from=builder \
    --chown=appuser:appuser \
    /install /usr/local

# Copy specific application files and folders safely
COPY --chown=appuser:appuser app.py .
COPY --chown=appuser:appuser static/ ./static/
COPY --chown=appuser:appuser templates/ ./templates/

EXPOSE 8080

USER appuser

# Pass App Version at build time
ARG APP_VERSION=v1.0.0
ENV APP_VERSION=${APP_VERSION}

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]