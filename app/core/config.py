"""Configuration objects for the Government Job Finder app."""

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


class Config:
    """Base configuration shared by all environments."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'gov_job_finder.sqlite3'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = os.getenv("WTF_CSRF_ENABLED", "true").lower() == "true"
    JOB_SOURCE_TIMEOUT_SECONDS = int(os.getenv("JOB_SOURCE_TIMEOUT_SECONDS", "20"))
    DAILY_SCRAPE_HOUR_UTC = int(os.getenv("DAILY_SCRAPE_HOUR_UTC", "3"))


class DevelopmentConfig(Config):
    """Configuration used for local development."""

    DEBUG = True


class TestingConfig(Config):
    """Configuration used by automated tests."""

    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    """Configuration used in deployed environments."""

    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
