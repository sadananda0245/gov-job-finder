"""Application extension instances.

Extensions are created once here and initialized by the Flask application
factory. Keeping them unbound at import time makes tests and multiple app
instances easier to manage.
"""

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
