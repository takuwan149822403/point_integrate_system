"""T01用pytest設定。"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from point_integrate_system.app import create_app  # noqa: E402


@pytest.fixture()
def app():
    """試験用Flaskアプリを返す。"""
    return create_app("testing")


@pytest.fixture()
def client(app):
    """試験用Flaskクライアントを返す。"""
    return app.test_client()
