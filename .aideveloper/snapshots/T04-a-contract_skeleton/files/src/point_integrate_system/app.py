"""Flaskアプリケーションファクトリ。"""
from __future__ import annotations

from .models import db
from flask import Flask, Response

from .config import get_config


def create_app(config_name: str | None = None) -> Flask:
    """Flaskアプリケーションを生成する。

    T01ではテンプレート、静的ファイル、DB、認証、業務サービスへ依存しない
    最小起動構成のみを提供する。
    """
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    @app.get("/")
    def index() -> Response:
        """テンプレート非依存のヘルスチェック兼ルート応答。"""
        return Response(
            "ポイント統合システムは起動しています。",
            status=200,
            mimetype="text/plain; charset=utf-8",
        )

    @app.errorhandler(404)
    def handle_not_found(error: object) -> tuple[Response, int]:
        """未定義URLへ簡潔な404応答を返す。"""
        return (
            Response(
                "指定されたページは見つかりません。",
                status=404,
                mimetype="text/plain; charset=utf-8",
            ),
            404,
        )

    db.init_app(app)

    from .routes import auth_bp
    app.register_blueprint(auth_bp)
    return app
