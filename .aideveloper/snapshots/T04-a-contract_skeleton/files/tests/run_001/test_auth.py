from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from point_integrate_system.app import create_app
from point_integrate_system.services import AuthService


@pytest.fixture()
def app():
    """試験区分: 正常系
    確認項目: create_app() がテスト用Flaskアプリを生成できる。
    """

    AuthService.reset_for_tests()
    flask_app = create_app("testing")
    flask_app.config.update(TESTING=True, SECRET_KEY="test-secret-key")
    return flask_app


@pytest.fixture()
def client(app):
    """試験区分: 正常系
    確認項目: Flask test_client を生成できる。
    """

    return app.test_client()


def test_create_app_and_client(app):
    """試験区分: 正常系
    確認項目: アプリケーションファクトリとtest_clientが利用可能である。
    """

    assert app is not None
    assert app.test_client() is not None


def test_root_redirects_by_auth_state(client):
    """試験区分: 正常系
    確認項目: GET / が未認証時は /login、認証済み時は /menu へリダイレクトする。
    """

    response = client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")

    login_response = client.post(
        "/login",
        data={"email": "dev.user@example.com", "password": "Password123!"},
    )
    assert login_response.status_code == 302

    response = client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/menu")


def test_register_login_logout_session_flow(client):
    """試験区分: 正常系
    確認項目: 登録、セッション維持、ログアウト、再ログインが成功する。
    """

    register_response = client.post(
        "/register",
        data={
            "name": "テストユーザー",
            "email": "new.user@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
        },
    )
    assert register_response.status_code == 302
    assert register_response.headers["Location"].endswith("/menu")

    menu_response = client.get("/menu")
    assert menu_response.status_code == 200
    assert "テストユーザー" in menu_response.get_data(as_text=True)

    logout_response = client.get("/logout")
    assert logout_response.status_code == 302
    assert logout_response.headers["Location"].endswith("/login")

    protected_response = client.get("/menu")
    assert protected_response.status_code == 302
    assert protected_response.headers["Location"].endswith("/login")

    login_response = client.post(
        "/login",
        data={"email": "new.user@example.com", "password": "Password123!"},
    )
    assert login_response.status_code == 302
    assert login_response.headers["Location"].endswith("/menu")


def test_login_screen_and_register_screen_render_assets(client):
    """試験区分: 正常系
    確認項目: ログイン画面と登録画面が200で表示されCSS/JSを参照する。
    """

    for path in ("/login", "/register"):
        response = client.get(path)
        html = response.get_data(as_text=True)
        assert response.status_code == 200
        assert "css/style.css" in html
        assert "js/main.js" in html


def test_invalid_login_returns_401_error_page(client):
    """試験区分: 異常系
    確認項目: 不正なログインはフォーム200再表示ではなく401エラー画面になる。
    """

    response = client.post(
        "/login",
        data={"email": "dev.user@example.com", "password": "wrong-password"},
    )
    html = response.get_data(as_text=True)
    assert response.status_code == 401
    assert "エラーが発生しました" in html
    assert "メールアドレスまたはパスワードが正しくありません" in html


def test_invalid_register_returns_422_error_page(client):
    """試験区分: 異常系
    確認項目: 登録入力不備は422エラー画面になる。
    """

    response = client.post(
        "/register",
        data={
            "name": "",
            "email": "bad-email",
            "password": "short",
            "confirm_password": "different",
        },
    )
    html = response.get_data(as_text=True)
    assert response.status_code == 422
    assert "エラーが発生しました" in html


def test_duplicate_register_returns_409_error_page(client):
    """試験区分: 異常系
    確認項目: 登録済みメールアドレスの再登録は409エラー画面になる。
    """

    data = {
        "name": "重複ユーザー",
        "email": "duplicate@example.com",
        "password": "Password123!",
        "confirm_password": "Password123!",
    }
    first = client.post("/register", data=data)
    assert first.status_code == 302
    client.get("/logout")

    second = client.post("/register", data=data)
    html = second.get_data(as_text=True)
    assert second.status_code == 409
    assert "既に登録されています" in html


def test_protected_design_routes_are_available_after_login(client):
    """試験区分: 正常系
    確認項目: screen_flow_designで示された主要GET画面が認証後に200で表示される。
    """

    client.post("/login", data={"email": "dev.user@example.com", "password": "Password123!"})
    for path in (
        "/menu",
        "/legacy-transfer",
        "/profile/edit",
        "/points/add",
        "/coupons",
        "/coupons/use",
        "/credit-card",
        "/family",
    ):
        response = client.get(path)
        assert response.status_code == 200, path


def test_public_password_reset_and_error_routes(client):
    """試験区分: 正常系
    確認項目: パスワード再設定関連と明示エラー画面が表示できる。
    """

    reset_request = client.get("/password-reset/request")
    assert reset_request.status_code == 200

    reset_token = client.get("/password-reset/sample-token")
    assert reset_token.status_code == 200

    error_response = client.get("/error?status=403")
    assert error_response.status_code == 403
    assert "HTTP 403" in error_response.get_data(as_text=True)


def test_404_route_behavior(client):
    """試験区分: 異常系
    確認項目: 未定義URLは404エラー画面で処理される。
    """

    response = client.get("/does-not-exist")
    html = response.get_data(as_text=True)
    assert response.status_code == 404
    assert "ページが見つかりません" in html


def test_static_assets_exist():
    """試験区分: 回帰
    確認項目: CSSとJavaScriptの静的ファイルが存在する。
    """

    package_root = ROOT / "src" / "point_integrate_system"
    assert (package_root / "static" / "css" / "style.css").exists()
    assert (package_root / "static" / "js" / "main.js").exists()


def test_auth_service_logic():
    """試験区分: 正常系
    確認項目: AuthService単体で登録・認証・ユーザー取得ができる。
    """

    AuthService.reset_for_tests()
    service = AuthService()
    user = service.register_user("サービス試験", "service@example.com", "Password123!", "Password123!")
    assert user["email"] == "service@example.com"
    assert "password_hash" not in user

    authenticated = service.authenticate("service@example.com", "Password123!")
    assert authenticated["id"] == user["id"]
    assert service.get_user(user["id"])["name"] == "サービス試験"


def test_display_definition_exists():
    """試験区分: 回帰
    確認項目: 画面定義書 display_difinition.md が生成されている。
    """

    assert (ROOT / "reports" / "run_001" / "display_difinition.md").exists()
