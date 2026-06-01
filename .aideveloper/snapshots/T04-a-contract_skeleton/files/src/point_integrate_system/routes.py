"""認証・セッション・ユーザー入口のルート定義。"""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from flask import Blueprint, Response, redirect, render_template, request, session, url_for
from werkzeug.exceptions import HTTPException

from .errors import AppError
from .forms import LoginForm, RegistrationForm
from .services import AuthService


auth_bp = Blueprint("auth", __name__)
auth_service = AuthService()


def render_error(status_code: int, message: str) -> tuple[str, int]:
    """エラー画面を指定ステータスで描画する。"""

    return render_template("error.html", status_code=status_code, message=message), status_code


def current_user() -> dict[str, Any] | None:
    """現在のセッションユーザーを取得する。"""

    return auth_service.get_user(session.get("user_id"))


def login_required(view: Callable[..., Any]) -> Callable[..., Any]:
    """未認証の場合はログイン画面へ遷移させるデコレーター。"""

    @wraps(view)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        if current_user() is None:
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


def _login_user(user: dict[str, Any]) -> None:
    """Flaskセッションへログイン状態を保存する。"""

    session.clear()
    session["user_id"] = user["id"]
    session["user_email"] = user["email"]
    session["user_name"] = user["name"]


@auth_bp.before_app_request
def redirect_root_by_auth_state() -> Response | None:
    """GET / を認証状態に応じて /login または /menu へ振り分ける。"""

    if request.path == "/" and request.method in {"GET", "HEAD"}:
        if current_user() is None:
            return redirect(url_for("auth.login"))
        return redirect(url_for("auth.menu"))
    return None


@auth_bp.app_errorhandler(AppError)
def handle_app_error(error: AppError) -> tuple[str, int]:
    """アプリケーション例外をエラー画面へ変換する。"""

    return render_error(error.status_code, error.message)


@auth_bp.app_errorhandler(404)
def handle_not_found(error: HTTPException) -> tuple[str, int]:
    """未定義URLを404エラー画面で返す。"""

    return render_error(404, "ページが見つかりません。")


@auth_bp.app_errorhandler(500)
def handle_internal_server_error(error: HTTPException) -> tuple[str, int]:
    """予期しないサーバーエラーを画面で返す。"""

    return render_error(500, "サーバー内部でエラーが発生しました。")


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> Any:
    """ログイン画面とログイン処理。"""

    if request.method == "GET":
        if current_user() is not None:
            return redirect(url_for("auth.menu"))
        return render_template("auth.html")

    try:
        form = LoginForm.from_mapping(request.form)
        user = auth_service.authenticate(form.email, form.password)
        _login_user(user)
        return redirect(url_for("auth.menu"))
    except AppError as exc:
        return render_error(exc.status_code, exc.message)


@auth_bp.route("/register", methods=["GET", "POST"])
def register() -> Any:
    """ユーザー登録画面と登録処理。"""

    if request.method == "GET":
        if current_user() is not None:
            return redirect(url_for("auth.menu"))
        return render_template("register.html")

    try:
        form = RegistrationForm.from_mapping(request.form)
        user = auth_service.register_user(
            name=form.name,
            email=form.email,
            password=form.password,
            confirm_password=form.confirm_password,
        )
        _login_user(user)
        return redirect(url_for("auth.menu"))
    except AppError as exc:
        return render_error(exc.status_code, exc.message)


@auth_bp.route("/logout", methods=["GET"])
def logout() -> Response:
    """ログアウトしてログイン画面へ戻る。"""

    session.clear()
    return redirect(url_for("auth.login"))


@auth_bp.route("/menu", methods=["GET"])
@login_required
def menu() -> str:
    """認証後のメニュー画面。"""

    return render_template("menu.html", user=current_user(), page_title="メニュー")


@auth_bp.route("/legacy-transfer", methods=["GET"])
@login_required
def legacy_transfer() -> str:
    """旧サービス連携入口。"""

    return render_template("menu.html", user=current_user(), page_title="legacy-transfer 画面")


@auth_bp.route("/profile/edit", methods=["GET"])
@login_required
def profile_edit() -> str:
    """プロフィール編集入口。"""

    return render_template("menu.html", user=current_user(), page_title="編集画面")


@auth_bp.route("/points/add", methods=["GET"])
@login_required
def points_add() -> str:
    """ポイント追加入口。"""

    return render_template("menu.html", user=current_user(), page_title="add 画面")


@auth_bp.route("/coupons", methods=["GET"])
@login_required
def coupons() -> str:
    """クーポン一覧入口。"""

    return render_template("menu.html", user=current_user(), page_title="coupons 画面")


@auth_bp.route("/coupons/use", methods=["GET"])
@login_required
def coupons_use() -> str:
    """クーポン利用入口。"""

    return render_template("menu.html", user=current_user(), page_title="use 画面")


@auth_bp.route("/credit-card", methods=["GET"])
@login_required
def credit_card() -> str:
    """クレジットカード入口。"""

    return render_template("menu.html", user=current_user(), page_title="credit-card 画面")


@auth_bp.route("/family", methods=["GET"])
@login_required
def family() -> str:
    """ファミリー共有入口。"""

    return render_template("menu.html", user=current_user(), page_title="family 画面")


@auth_bp.route("/password-reset/request", methods=["GET"])
def password_reset_request() -> str:
    """パスワード再設定依頼画面。"""

    return render_template("auth.html", page_title="パスワード再設定", info_message="パスワード再設定機能は準備中です。")


@auth_bp.route("/password-reset/<token>", methods=["GET"])
def password_reset_token(token: str) -> Any:
    """パスワード再設定トークン画面。"""

    clean_token = (token or "").strip()
    if not clean_token or len(clean_token) > 120:
        return render_error(422, "パスワード再設定トークンが正しくありません。")
    return render_template("auth.html", page_title="パスワード再設定", info_message="新しいパスワード設定機能は準備中です。")


@auth_bp.route("/error", methods=["GET"])
def error_page() -> tuple[str, int]:
    """開発時確認用のエラー画面。"""

    raw_status = request.args.get("status", "400")
    try:
        status_code = int(raw_status)
    except ValueError:
        status_code = 400
    if status_code < 400 or status_code > 599:
        status_code = 400
    return render_error(status_code, "エラー画面です。")
