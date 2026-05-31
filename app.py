"""ポイント統合システムの開発用起動エントリポイント。"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from point_integrate_system.app import create_app  # noqa: E402


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する。"""
    parser = argparse.ArgumentParser(description="ポイント統合システムを起動します。")
    parser.add_argument("--host", default="127.0.0.1", help="待ち受けホスト。既定値: 127.0.0.1")
    parser.add_argument("--port", default=5050, type=int, help="待ち受けポート。既定値: 5050")
    parser.add_argument("--config", default=None, help="設定名。例: development, testing, production")
    return parser.parse_args()


def main() -> None:
    """Flaskアプリケーションを起動する。"""
    args = parse_args()
    app = create_app(args.config)
    app.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
