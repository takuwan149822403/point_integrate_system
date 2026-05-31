from __future__ import annotations

from flask import Flask

from point_integrate_system import create_app


def test_create_app_succeeds() -> None:
    """試験区分: 正常系 / 確認項目: create_app()がFlaskアプリを生成できること。"""
    app = create_app()
    assert isinstance(app, Flask)


def test_create_app_testing_config_succeeds() -> None:
    """試験区分: 正常系 / 確認項目: create_app('testing')で試験設定が有効になること。"""
    app = create_app('testing')
    assert app.config['TESTING'] is True


def test_test_client_can_be_created(app: Flask) -> None:
    """試験区分: 正常系 / 確認項目: Flask test_clientを作成できること。"""
    client = app.test_client()
    assert client is not None


def test_root_returns_200_without_template(client) -> None:
    """試験区分: 正常系 / 確認項目: GET / がリダイレクトせずtemplate非依存で200を返すこと。"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.mimetype == 'text/plain'
    assert b'point_integrate_system is running.' in response.data


def test_unknown_route_returns_404(client) -> None:
    """試験区分: 異常系 / 確認項目: 未定義URLがプレーンテキストの404を返すこと。"""
    response = client.get('/does-not-exist')
    assert response.status_code == 404
    assert response.mimetype == 'text/plain'
