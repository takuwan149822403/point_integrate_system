# ポイント統合システム

Flaskを利用したポイント統合システムです。

## T01: 最小起動構成

この段階では、アプリケーションファクトリと起動エントリポイントのみを実装しています。

- `create_app()` を import できます。
- `python app.py` または `py app.py` で起動できます。
- 既定の起動先は `127.0.0.1:5050` です。
- `GET /` はテンプレート、静的ファイル、DB、認証へ依存せず、HTTP 200を返します。

## セットアップ

```bash
python -m venv .venv
. .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate
pip install -r requirements.txt
```

## 起動

```bash
python app.py
```

ホストやポートを指定する場合:

```bash
python app.py --host 127.0.0.1 --port 5050
```

## 設定

主な環境変数:

- `FLASK_CONFIG`: `development`, `testing`, `production` のいずれか
- `SECRET_KEY`: Flaskの秘密鍵。本番では必ず安全な値を設定してください。
- `FLASK_DEBUG`: `1`, `true`, `yes`, `on` の場合にデバッグを有効化します。

## テスト

```bash
pytest tests/run_001
```

## 今後の実装範囲

テンプレート、静的ファイル、DB、認証、業務ルートは後続タスクで追加します。
