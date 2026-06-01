"""T01のFlask基盤・起動構成の試験。"""
from __future__ import annotations

from flask import Flask

from point_integrate_system.app import create_app
from point_integrate_system.config import TestingConfig, get_config


def test_create_app_succeeds() -> None:
    """試験区分: 正常系
    確認項目: create_app() がFlaskアプリケーションを返すこと。
    """
    app = create_app("testing")

    assert isinstance(app, Flask)
    assert app.testing is True


def test_test_client_can_be_created(app: Flask) -> None:
    """試験区分: 正常系
    確認項目: Flask test_clientを生成できること。
    """
    client = app.test_client()

    assert client is not None


def test_root_returns_200_without_redirect_or_template(client) -> None:
    """試験区分: 正常系
    確認項目: GET / がリダイレクトせず、テンプレート非依存でHTTP 200を返すこと。
    """
    response = client.get("/")

    assert response.status_code == 200
    assert response.location is None
    assert "ポイント統合システム" in response.get_data(as_text=True)


def test_missing_route_returns_plain_404(client) -> None:
    """試験区分: 異常系
    確認項目: 未定義URLがテンプレート非依存のHTTP 404を返すこと。
    """
    response = client.get("/does-not-exist")

    assert response.status_code == 404
    assert "見つかりません" in response.get_data(as_text=True)


def test_testing_config_lookup() -> None:
    """試験区分: 正常系
    確認項目: testing設定名からTestingConfigを取得できること。
    """
    assert get_config("testing") is TestingConfig
