# point_integrate_system

ポイント統合システムのFlaskアプリケーションです。

## T01: Flask基盤・起動構成

この段階では、アプリケーションファクトリと開発用起動エントリポイントのみを提供します。

- `create_app()` を `point_integrate_system` からimportできます。
- `GET /` はテンプレート、静的ファイル、DB、認証に依存せず、HTTP 200を返します。
- `py app.py` または `python app.py` で `127.0.0.1:5050` に起動します。

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

ホストとポートを指定する場合:

```bash
python app.py --host 127.0.0.1 --port 5050
```

## 設定

設定名は環境変数またはCLI引数で指定できます。

```bash
python app.py --config testing
```

利用可能な設定名:

- `development`
- `testing`
- `production`

`SECRET_KEY` は環境変数から読み込みます。開発・試験用の安全な既定値はありますが、本番環境では必ず環境変数で設定してください。

## T01で未実装のもの

以下は後続タスクで実装するため、T01では意図的に含めていません。

- テンプレート
- CSS/JavaScriptなどの静的ファイル
- DBモデルとRepository
- 認証・セッション
- 業務サービスと画面遷移
