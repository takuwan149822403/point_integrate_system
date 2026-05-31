from __future__ import annotations

from flask import Flask, Response

from .config import get_config


PACKAGE_NAME = 'point_integrate_system'


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    @app.get('/')
    def index() -> Response:
        return Response('point_integrate_system is running.\n', status=200, mimetype='text/plain; charset=utf-8')

    @app.errorhandler(404)
    def handle_not_found(error: object) -> tuple[Response, int]:
        return Response('ページが見つかりません。\n', status=404, mimetype='text/plain; charset=utf-8'), 404

    return app
