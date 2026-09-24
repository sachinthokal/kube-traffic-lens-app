# ================================
# App Builder OS
# ================================
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir \
    --prefix=/install \
    -r requirements.txt


# ================================
# App Runtime OS
# ================================
FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd appuser

# Copy dependencies from builder
COPY --from=builder \
    --chown=appuser:appuser \
    /install /usr/local

# Copy application
COPY --chown=appuser:appuser . .

EXPOSE 8080

USER appuser

# Pass App Version at build time
ARG APP_VERSION=v1.0.0
ENV APP_VERSION=${APP_VERSION}

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]