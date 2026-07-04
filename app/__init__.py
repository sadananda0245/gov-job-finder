"""Application factory for Government Job Finder."""

from flask import Flask

from app.core.config import config_by_name
from app.routes import register_routes
from extensions import csrf, db, login_manager, migrate


def create_app(config_name: str = "default") -> Flask:
    """Create and configure a Flask application instance."""

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["default"]))

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"

    register_routes(app)
    return app
