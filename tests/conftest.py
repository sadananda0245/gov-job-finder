"""Pytest fixtures for Government Job Finder."""

import pytest

from app import create_app


@pytest.fixture()
def app():
    """Create a Flask test app."""

    return create_app("testing")


@pytest.fixture()
def client(app):
    """Create a Flask test client."""

    return app.test_client()
