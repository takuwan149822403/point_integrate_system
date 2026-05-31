from __future__ import annotations

import argparse
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from point_integrate_system.app import create_app  # noqa: E402


def _positive_port(value: str) -> int:
    try:
        port = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError('ポート番号は整数で指定してください。') from exc
    if port < 1 or port > 65535:
        raise argparse.ArgumentTypeError('ポート番号は1から65535の範囲で指定してください。')
    return port


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='ポイント統合システムの開発用Flaskサーバーを起動します。')
    parser.add_argument('--host', default='127.0.0.1', help='待ち受けホスト。既定値は127.0.0.1です。')
    parser.add_argument('--port', default=5050, type=_positive_port, help='待ち受けポート。既定値は5050です。')
    parser.add_argument('--config', default=None, help='設定名。development/testing/productionを指定できます。')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = create_app(args.config)
    app.run(host=args.host, port=args.port)


if __name__ == '__main__':
    main()
