"""Route registration helpers."""

from flask import Flask

from app.routes.home import home_bp


def register_routes(app: Flask) -> None:
    """Register all application blueprints."""

    app.register_blueprint(home_bp)
