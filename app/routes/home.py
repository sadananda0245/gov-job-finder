"""Home routes for the Government Job Finder app."""

from flask import Blueprint, jsonify


home_bp = Blueprint("home", __name__)


@home_bp.get("/")
def index():
    """Return a small health payload until the dashboard is implemented."""

    return jsonify(
        {
            "service": "Government Job Finder",
            "status": "ok",
            "message": "Track official government job notifications and eligibility matches.",
        }
    )


@home_bp.get("/health")
def health():
    """Return a machine-readable health check response."""

    return jsonify({"status": "ok"})
