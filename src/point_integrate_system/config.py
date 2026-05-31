from __future__ import annotations

import os
from typing import Type


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


class Config:
    # 開発専用の既定値です。本番環境では必ずSECRET_KEYを環境変数で設定してください。
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-only-change-me')
    TESTING = False
    DEBUG = _env_bool('DEBUG', False)
    JSON_AS_ASCII = False


class DevelopmentConfig(Config):
    DEBUG = _env_bool('DEBUG', True)


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'testing-secret-key')


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', '')


config_by_name: dict[str, Type[Config]] = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}


def get_config(config_name: str | None = None) -> Type[Config]:
    selected_name = config_name or os.environ.get('FLASK_CONFIG') or os.environ.get('APP_CONFIG') or 'default'
    return config_by_name.get(selected_name, DevelopmentConfig)
