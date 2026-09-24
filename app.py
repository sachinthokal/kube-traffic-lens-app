"""Kube Traffic Lens Flask application."""
import logging
import os
import socket

from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Configure application logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="[%(asctime)s +0530] [%(process)d] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

# Read application details from environment variables
APP_VERSION = os.getenv("APP_VERSION", "v1.0.0")
APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT", "local")
APP_NAME = os.getenv("APP_NAME", "kube-traffic-lens")

# Current pod/container hostname
POD_NAME = socket.gethostname()


@app.route("/")
def index():
    """Render the application landing page."""
    logger.info(
        "Homepage requested | version=%s environment=%s pod=%s",
        APP_VERSION,
        APP_ENVIRONMENT,
        POD_NAME,
    )

    return render_template(
        "index.html",
        version=APP_VERSION,
        pod=POD_NAME,
        app_name=APP_NAME,
        env=APP_ENVIRONMENT,
    )


@app.route("/health")
def health():
    """Health endpoint for liveness checks."""
    logger.debug("Health check requested | pod=%s", POD_NAME)

    return jsonify({
        "status": "UP"
    }), 200


@app.route("/ready")
def ready():
    """Readiness endpoint for traffic routing."""
    logger.debug("Readiness check requested | pod=%s", POD_NAME)

    return jsonify({
        "status": "READY",
        "acceptingTraffic": True
    }), 200


@app.route("/api/details")
def details():
    """Return application and runtime details."""
    logger.info(
        "Details requested | version=%s environment=%s pod=%s",
        APP_VERSION,
        APP_ENVIRONMENT,
        POD_NAME,
    )

    return jsonify({
        "application": APP_NAME,
        "version": APP_VERSION,
        "environment": APP_ENVIRONMENT,
        "pod": POD_NAME,
        "hostname": POD_NAME,
    }), 200


if __name__ == "__main__":
    logger.info(
        "Starting application | version=%s environment=%s",
        APP_VERSION,
        APP_ENVIRONMENT,
    )

    app.run(host="0.0.0.0", port=8080)
