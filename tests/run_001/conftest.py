from __future__ import annotations

import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from point_integrate_system import create_app  # noqa: E402


@pytest.fixture()
def app():
    app_instance = create_app('testing')
    return app_instance


@pytest.fixture()
def client(app):
    return app.test_client()
