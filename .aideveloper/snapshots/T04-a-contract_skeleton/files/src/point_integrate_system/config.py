"""Flask設定定義。"""
from __future__ import annotations

import os
from typing import Type


def _env_bool(name: str, default: bool = False) -> bool:
    """環境変数を真偽値として解釈する。"""
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    """共通設定。

    SECRET_KEYは本番では必ず環境変数から設定すること。既定値は開発・テスト用の
    安全なフォールバックであり、本番利用を意図しない。
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    DEBUG = _env_bool("FLASK_DEBUG", False)
    TESTING = False
    JSON_AS_ASCII = False


class DevelopmentConfig(Config):
    """ローカル開発向け設定。"""

    DEBUG = _env_bool("FLASK_DEBUG", True)


class TestingConfig(Config):
    """自動試験向け設定。"""
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    TESTING = True
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "testing-secret-key")


class ProductionConfig(Config):
    """本番向け設定。"""

    DEBUG = False


config_by_name: dict[str, Type[Config]] = {
    "default": DevelopmentConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(config_name: str | None = None) -> Type[Config]:
    """設定名に対応する設定クラスを返す。"""
    selected_name = config_name or os.environ.get("FLASK_CONFIG", "default")
    return config_by_name.get(selected_name, DevelopmentConfig)
