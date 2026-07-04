"""Development entry point for Government Job Finder."""

import os

from app import create_app


app = create_app(os.getenv("FLASK_ENV", "default"))


if __name__ == "__main__":
    app.run()
