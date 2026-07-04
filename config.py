"""Backward-compatible configuration exports."""

from app.core.config import Config, DevelopmentConfig, ProductionConfig, TestingConfig, config_by_name

__all__ = [
    "Config",
    "DevelopmentConfig",
    "ProductionConfig",
    "TestingConfig",
    "config_by_name",
]
