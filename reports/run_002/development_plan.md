# 製造・試験マネージャー計画書

## 1. 判定結果

- システム名: `point_integrate_system`
- project_mode: `python_flask`
- 複雑度: `large`
- 生成方式: `staged`
- 複雑度スコア: `13`
- 判定理由: inputが長文、URL/画面候補が多い、DBあり、Webあり、認証あり、通知/メールあり、共有状態/グループ処理あり、JSON/XML連携あり、複数業務ワークフローあり のため generation_mode=staged と判定。

## 2. 簡易画面設計・画面遷移契約

この節は、製造・試験・修復フェーズで仕様が揺れないようにするための簡易版画面設計である。詳細仕様は後続の display_difinition.md で確定する。

### 画面・HTTP既定方針

- Issueで明示がない限り、GET / は単なるランディングページにしない。未認証なら /login、認証済みなら /menu へリダイレクトする。
- Issueで明示がない限り、認証・登録・権限・セッション系の異常入力は通常フォームの200再表示で握りつぶさず、400/401/403/409/422等の適切なHTTPステータスと対応するエラー画面で扱う。
- 生成テストはscreen_flow_designを期待値にする。

### 画面一覧

| 画面ID | URL | Method | 機能概要 | 遷移先/遷移条件 | エラー方針 |
|---|---|---|---|---|---|
| `explicit_register_1` | `/register` | GET | Issue/設計書に現れたURL。詳細挙動が未記載の場合はManagerが画面遷移を補完する。 | Issue explicit route; preserve URL/method contract | Issueで明示されたHTTP方針があれば優先。未指定ならbehavior_defaultsに従う。 |
| `explicit_legacy_transfer_2` | `/legacy-transfer` | GET | Issue/設計書に現れたURL。詳細挙動が未記載の場合はManagerが画面遷移を補完する。 | Issue explicit route; preserve URL/method contract | Issueで明示されたHTTP方針があれば優先。未指定ならbehavior_defaultsに従う。 |
| `explicit_login_3` | `/login` | GET | Issue/設計書に現れたURL。詳細挙動が未記載の場合はManagerが画面遷移を補完する。 | Issue explicit route; preserve URL/method contract | Issueで明示されたHTTP方針があれば優先。未指定ならbehavior_defaultsに従う。 |
| `explicit_logout_4` | `/logout` | GET | Issue/設計書に現れたURL。詳細挙動が未記載の場合はManagerが画面遷移を補完する。 | Issue explicit route; preserve URL/method contract | Issueで明示されたHTTP方針があれば優先。未指定ならbehavior_defaultsに従う。 |
| `explicit_menu_5` | `/menu` | GET | Issue/設計書に現れたURL。詳細挙動が未記載の場合はManagerが画面遷移を補完する。 | Issue explicit route; preserve URL/method contract | Issueで明示されたHTTP方針があれば優先。未指定ならbehavior_defaultsに従う。 |
| `explicit_profile_edit_6` | `/profile/edit` | GET | Issue/設計書に現れたURL。詳細挙動が未記載の場合はManagerが画面遷移を補完する。 | Issue explicit route; preserve URL/method contract | Issueで明示されたHTTP方針があれば優先。未指定ならbehavior_defaultsに従う。 |
| `explicit_points_add_7` | `/points/add` | GET | Issue/設計書に現れたURL。詳細挙動が未記載の場合はManagerが画面遷移を補完する。 | Issue explicit route; preserve URL/method contract | Issueで明示されたHTTP方針があれば優先。未指定ならbehavior_defaultsに従う。 |
| `explicit_coupons_8` | `/coupons` | GET | Issue/設計書に現れたURL。詳細挙動が未記載の場合はManagerが画面遷移を補完する。 | Issue explicit route; preserve URL/method contract | Issueで明示されたHTTP方針があれば優先。未指定ならbehavior_defaultsに従う。 |
| `explicit_coupons_use_9` | `/coupons/use` | GET | Issue/設計書に現れたURL。詳細挙動が未記載の場合はManagerが画面遷移を補完する。 | Issue explicit route; preserve URL/method contract | Issueで明示されたHTTP方針があれば優先。未指定ならbehavior_defaultsに従う。 |
| `explicit_credit_card_10` | `/credit-card` | GET | Issue/設計書に現れたURL。詳細挙動が未記載の場合はManagerが画面遷移を補完する。 | Issue explicit route; preserve URL/method contract | Issueで明示されたHTTP方針があれば優先。未指定ならbehavior_defaultsに従う。 |
| `explicit_family_11` | `/family` | GET | Issue/設計書に現れたURL。詳細挙動が未記載の場合はManagerが画面遷移を補完する。 | Issue explicit route; preserve URL/method contract | Issueで明示されたHTTP方針があれば優先。未指定ならbehavior_defaultsに従う。 |
| `explicit_password_reset_request_12` | `/password-reset/request` | GET | Issue/設計書に現れたURL。詳細挙動が未記載の場合はManagerが画面遷移を補完する。 | Issue explicit route; preserve URL/method contract | Issueで明示されたHTTP方針があれば優先。未指定ならbehavior_defaultsに従う。 |
| `explicit_password_reset_token_13` | `/password-reset/<token>` | GET | Issue/設計書に現れたURL。詳細挙動が未記載の場合はManagerが画面遷移を補完する。 | Issue explicit route; preserve URL/method contract | Issueで明示されたHTTP方針があれば優先。未指定ならbehavior_defaultsに従う。 |
| `explicit_error_14` | `/error` | GET | Issue/設計書に現れたURL。詳細挙動が未記載の場合はManagerが画面遷移を補完する。 | Issue explicit route; preserve URL/method contract | Issueで明示されたHTTP方針があれば優先。未指定ならbehavior_defaultsに従う。 |
| `root_entry` | `/` | GET | 認証状態に応じて次画面へ振り分ける入口。 | 未認証 -> /login<br>認証済み -> /menu | Issue未指定のためManagerが補完した既定方針。 |
| `error` | `/error or rendered error.html` | GET/render | 認証・登録・権限・セッション異常時の表示先。 | recover -> /login or /register | Issue未指定のためManagerが補完した既定方針。 |

## 3. 開発時アクセス・DB・モジュール契約

この節は、T02以降のDB設計、T04以降のService/Model連携、import/exportの揺れを防ぐための固定契約である。CodeWriter、試験、修復はこの契約を優先する。

### 開発時アクセス設計

| 名称 | URL | Method | 用途 |
|---|---|---|---|
| ユーザー登録画面 | `/register` | GET | Issue/設計書に現れた開発時確認URL |
| legacy-transfer 画面 | `/legacy-transfer` | GET | Issue/設計書に現れた開発時確認URL |
| ログイン画面 | `/login` | GET | Issue/設計書に現れた開発時確認URL |
| ログアウト | `/logout` | GET | Issue/設計書に現れた開発時確認URL |
| メニュー画面 | `/menu` | GET | Issue/設計書に現れた開発時確認URL |
| 編集画面 | `/profile/edit` | GET | Issue/設計書に現れた開発時確認URL |
| add 画面 | `/points/add` | GET | Issue/設計書に現れた開発時確認URL |
| coupons 画面 | `/coupons` | GET | Issue/設計書に現れた開発時確認URL |
| use 画面 | `/coupons/use` | GET | Issue/設計書に現れた開発時確認URL |
| credit-card 画面 | `/credit-card` | GET | Issue/設計書に現れた開発時確認URL |
| family 画面 | `/family` | GET | Issue/設計書に現れた開発時確認URL |
| request 画面 | `/password-reset/request` | GET | Issue/設計書に現れた開発時確認URL |
| <token> 画面 | `/password-reset/<token>` | GET | Issue/設計書に現れた開発時確認URL |
| error 画面 | `/error` | GET | Issue/設計書に現れた開発時確認URL |
| root_entry | `/` | GET | 未認証は/login、認証済みは/menuへ振り分ける入口 |

開発用仮アカウント:
- role=standard_user / email=`dev.user@example.com` / password=`Password123!` / scope=local test / GitHub Actions only

### DBテーブル設計

SQLAlchemy設定契約:
- `Config`: ['SQLALCHEMY_DATABASE_URI', 'SQLALCHEMY_TRACK_MODIFICATIONS']
- `TestingConfig`: {'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:', 'TESTING': True}
- `DevelopmentConfig`: DATABASE_URL env fallback to local SQLite
- `ProductionConfig`: DATABASE_URL env required or explicitly documented fallback

#### User / `users`

- 目的: 認証・セッションの主体ユーザー
- constructor_fields: `name`, `email`, `password_hash`, `is_active`
- 禁止別名 -> 正規フィールド: `password` -> `password_hash`, `mail` -> `email`

| Field | Type | Nullable | 備考 |
|---|---|---|---|
| `id` | Integer |  | PK |
| `name` | String(120) | False | - |
| `email` | String(255) | False | UNIQUE |
| `password_hash` | String(255) | False | - |
| `is_active` | Boolean | False | default=True |
| `created_at` | DateTime | False | - |
| `updated_at` | DateTime | False | - |

#### PointAccount / `point_accounts`

- 目的: ポイント残高・アカウント状態
- constructor_fields: `user_id`, `balance`, `status`
- 禁止別名 -> 正規フィールド: `points` -> `balance`

| Field | Type | Nullable | 備考 |
|---|---|---|---|
| `id` | Integer |  | PK |
| `user_id` | Integer | False | FK users.id |
| `balance` | Integer | False | default=0 |
| `status` | String(32) | False | default=active |
| `created_at` | DateTime | False | - |
| `updated_at` | DateTime | False | - |

#### PointTransaction / `point_transactions`

- 目的: ポイント増減・履歴
- constructor_fields: `user_id`, `point_delta`, `transaction_type`, `description`
- 禁止別名 -> 正規フィールド: `points` -> `point_delta`, `note` -> `description`, `related_member_id` -> `user_id`

| Field | Type | Nullable | 備考 |
|---|---|---|---|
| `id` | Integer |  | PK |
| `user_id` | Integer | False | FK users.id |
| `point_delta` | Integer | False | - |
| `transaction_type` | String(32) | False | - |
| `description` | String(255) | True | - |
| `created_at` | DateTime | False | - |

#### Coupon / `coupons`

- 目的: クーポン・特典
- constructor_fields: `user_id`, `title`, `status`, `description`
- 禁止別名 -> 正規フィールド: `name` -> `title`, `note` -> `description`

| Field | Type | Nullable | 備考 |
|---|---|---|---|
| `id` | Integer |  | PK |
| `user_id` | Integer | False | FK users.id |
| `title` | String(160) | False | - |
| `status` | String(32) | False | default=active |
| `description` | Text | True | - |
| `created_at` | DateTime | False | - |
| `updated_at` | DateTime | False | - |

#### Rank / `ranks`

- 目的: ランク・会員グレード
- constructor_fields: `user_id`, `title`, `status`, `description`
- 禁止別名 -> 正規フィールド: `name` -> `title`, `note` -> `description`

| Field | Type | Nullable | 備考 |
|---|---|---|---|
| `id` | Integer |  | PK |
| `user_id` | Integer | False | FK users.id |
| `title` | String(160) | False | - |
| `status` | String(32) | False | default=active |
| `description` | Text | True | - |
| `created_at` | DateTime | False | - |
| `updated_at` | DateTime | False | - |

#### Order / `orders`

- 目的: 注文・申請・依頼
- constructor_fields: `user_id`, `title`, `status`, `description`
- 禁止別名 -> 正規フィールド: `name` -> `title`, `note` -> `description`

| Field | Type | Nullable | 備考 |
|---|---|---|---|
| `id` | Integer |  | PK |
| `user_id` | Integer | False | FK users.id |
| `title` | String(160) | False | - |
| `status` | String(32) | False | default=active |
| `description` | Text | True | - |
| `created_at` | DateTime | False | - |
| `updated_at` | DateTime | False | - |

#### Payment / `payments`

- 目的: 支払い・決済
- constructor_fields: `user_id`, `title`, `status`, `description`
- 禁止別名 -> 正規フィールド: `name` -> `title`, `note` -> `description`

| Field | Type | Nullable | 備考 |
|---|---|---|---|
| `id` | Integer |  | PK |
| `user_id` | Integer | False | FK users.id |
| `title` | String(160) | False | - |
| `status` | String(32) | False | default=active |
| `description` | Text | True | - |
| `created_at` | DateTime | False | - |
| `updated_at` | DateTime | False | - |

#### Notification / `notifications`

- 目的: 通知
- constructor_fields: `user_id`, `event_type`, `payload_json`
- 禁止別名 -> 正規フィールド: `payload` -> `payload_json`, `type` -> `event_type`

| Field | Type | Nullable | 備考 |
|---|---|---|---|
| `id` | Integer |  | PK |
| `user_id` | Integer | False | FK users.id |
| `event_type` | String(64) | False | - |
| `payload_json` | Text | True | - |
| `created_at` | DateTime | False | - |

#### UserGroup / `user_groups`

- 目的: 共有・グループ状態
- constructor_fields: `name`, `owner_user_id`
- 禁止別名 -> 正規フィールド: `owner_id` -> `owner_user_id`

| Field | Type | Nullable | 備考 |
|---|---|---|---|
| `id` | Integer |  | PK |
| `name` | String(120) | False | - |
| `owner_user_id` | Integer | False | FK users.id |
| `created_at` | DateTime | False | - |

### Module import/export契約

| Module | Public exports |
|---|---|
| `src/point_integrate_system/config.py` | `Config`, `DevelopmentConfig`, `TestingConfig`, `ProductionConfig`, `config_by_name`, `get_config` |
| `src/point_integrate_system/errors.py` | `AppError`, `AuthError`, `RegistrationError`, `LoginError`, `PermissionError`, `ConflictError`, `DomainServiceError`, `PersistenceError` |
| `src/point_integrate_system/app.py` | `create_app` |
| `src/point_integrate_system/services.py` | `AuthService`, `DomainService` |
| `src/point_integrate_system/models.py` | `db`, `User`, `PointAccount`, `PointTransaction`, `Coupon`, `Rank`, `Order`, `Payment`, `Notification`, `UserGroup` |
| `src/point_integrate_system/repositories.py` | `UserRepository`, `PointAccountRepository`, `PointTransactionRepository`, `CouponRepository`, `RankRepository`, `OrderRepository`, `PaymentRepository`, `NotificationRepository`, `UserGroupRepository`, `RepositoryError` |

### Service / Model バインディング契約

| Model | Allowed constructor keywords | 禁止別名 |
|---|---|---|
| `User` | `name`, `email`, `password_hash`, `is_active` | `password`→`password_hash`, `mail`→`email` |
| `PointAccount` | `user_id`, `balance`, `status` | `points`→`balance` |
| `PointTransaction` | `user_id`, `point_delta`, `transaction_type`, `description` | `points`→`point_delta`, `note`→`description`, `related_member_id`→`user_id` |
| `Coupon` | `user_id`, `title`, `status`, `description` | `name`→`title`, `note`→`description` |
| `Rank` | `user_id`, `title`, `status`, `description` | `name`→`title`, `note`→`description` |
| `Order` | `user_id`, `title`, `status`, `description` | `name`→`title`, `note`→`description` |
| `Payment` | `user_id`, `title`, `status`, `description` | `name`→`title`, `note`→`description` |
| `Notification` | `user_id`, `event_type`, `payload_json` | `payload`→`payload_json`, `type`→`event_type` |
| `UserGroup` | `name`, `owner_user_id` | `owner_id`→`owner_user_id` |

## 3.5 モジュールimport依存方向契約

- パッケージ名統一定義:
  - `source_root`: `src`
  - `package`: `point_integrate_system`
  - `import_root`: `point_integrate_system`
  - `app_factory_module`: `point_integrate_system.app`
  - `routes_module`: `point_integrate_system.routes`
  - `models_module`: `point_integrate_system.models`
  - `services_module`: `point_integrate_system.services`
  - `repositories_module`: `point_integrate_system.repositories`
  - `errors_module`: `point_integrate_system.errors`

- import依存方向:
  - `src/point_integrate_system/app.py -> src/point_integrate_system/config.py`
  - `src/point_integrate_system/app.py -> src/point_integrate_system/models.py`
  - `src/point_integrate_system/app.py -> src/point_integrate_system/routes.py`
  - `src/point_integrate_system/routes.py -> src/point_integrate_system/forms.py`
  - `src/point_integrate_system/routes.py -> src/point_integrate_system/services.py`
  - `src/point_integrate_system/routes.py -> src/point_integrate_system/errors.py`
  - `src/point_integrate_system/services.py -> src/point_integrate_system/repositories.py`
  - `src/point_integrate_system/services.py -> src/point_integrate_system/models.py`
  - `src/point_integrate_system/services.py -> src/point_integrate_system/errors.py`
  - `src/point_integrate_system/repositories.py -> src/point_integrate_system/models.py`
  - `src/point_integrate_system/repositories.py -> src/point_integrate_system/errors.py`
  - `tests/run_XXX -> src/point_integrate_system/app.py`
  - `tests/run_XXX -> src/point_integrate_system/models.py`
  - `tests/run_XXX -> src/point_integrate_system/repositories.py`
  - `tests/run_XXX -> src/point_integrate_system/services.py`

- 依存ルール:
  - Imports should follow the arrow direction. Avoid reverse imports that create cycles.
  - models.py must not import routes.py/services.py/repositories.py.
  - repositories.py must not import routes.py or app.py.
  - services.py must not import routes.py or app.py.
  - routes.py may call services/forms/errors, but should not directly own persistence transaction policy.
  - app.py wires config/db/blueprints and should avoid business logic.
  - If a new local module is introduced, add its import direction to this design and keep module_contract_design exports aligned.

## 4. 製造タスク分割

| タスクID | タスク名 | カテゴリ | 依存 | 主な目的 |
|---|---|---|---|---|
| `T01` | Flask基盤・起動構成 | scaffold | - | root app.py / src app.py / create_app / config / README の最小起動構成を作成する。T01ではtemplate/static/DB/authに依存しないGET / 200応答に限定する。 |
| `T02` | 永続化モデル・Repository | persistence | T01 | SQLAlchemyモデル、DB初期化、Repository層を作成する。 |
| `T03` | 認証・セッション・ユーザー入口 | auth | T01, T02 | 登録、ログイン、ログアウト、セッション維持、認証前後の画面遷移を実装する。Issueで明示がない場合も、GET / は単なるランディングページにせず、未認証なら /login、認証済みなら /menu へリダイレクトする。認証系の異常入力は 400/401/403/409/422 等の適切なHTTPステータスと対応するエラー画面で扱う。 |
| `T04` | 主要業務ワークフロー | domain | T01, T02, T03 | 要件の中核となる業務ロジック、状態更新、計算、一覧/詳細表示を実装する。 |
| `T05` | 通知・外部通信境界 | communication | T01, T02, T03, T04 | メール送信、通知、デバッグモード時の疑似送信、非デバッグ時の実送信境界を実装する。 |
| `T06` | グループ・共有状態管理 | grouping | T01, T02, T03, T04 | 複数ユーザーまたは複数要素のグループ化、共有状態、統合処理を実装する。 |
| `T07` | 画面・静的ファイル・画面仕様書 | ui | T01, T04 | HTML/CSS/JavaScriptとdisplay_difinition.mdを整備する。 |
| `T08` | JSON/XMLインターフェース | interface | T01, T04 | JSON/XMLシリアライズ、サンプルデータ、interface_difinition.mdを実装する。 |
| `T09` | 全体結合・README・最終補強 | integration | T01, T02, T03, T04, T05, T06, T07, T08 | 全体のimport、起動、代表フロー、README、テスト整合を補強する。 |

## 5. タスク別作成範囲

### T01 Flask基盤・起動構成

- 目的: root app.py / src app.py / create_app / config / README の最小起動構成を作成する。T01ではtemplate/static/DB/authに依存しないGET / 200応答に限定する。
- 依存: -
- 主な作成・修正対象:
  - `app.py`
  - `src/app.py`
  - `src/point_integrate_system/__init__.py`
  - `src/point_integrate_system/app.py`
  - `src/point_integrate_system/config.py`
  - `requirements.txt`
  - `pyproject.toml`
  - `README.md`
- 完了条件:
  - py app.py または python app.py で起動できる。
  - create_app() をimportできる。
  - GET / はtemplate非依存で200を返す。
- 禁止/注意事項:
  - 既存の完了済みタスク成果物を全面再生成しない。
  - 現在のタスク範囲外の大規模リファクタリングを行わない。
  - root entrypoint、設定、DB初期化方式を理由なく破壊しない。
  - 要件にない外部システム、DB、Web、画像出力を勝手に追加しない。
  - allowed_filesにないファイルを修正する場合はsummaryに理由を書く。

### T02 永続化モデル・Repository

- 目的: SQLAlchemyモデル、DB初期化、Repository層を作成する。
- 依存: T01
- 主な作成・修正対象:
  - `src/point_integrate_system/models.py`
  - `src/point_integrate_system/repositories.py`
  - `src/point_integrate_system/app.py`
  - `src/point_integrate_system/config.py`
  - `tests/run_XXX/test_models.py`
  - `tests/run_XXX/test_repositories.py`
- 完了条件:
  - DB初期化が成功する。
  - 主要モデルを作成・保存・検索できる。
- 禁止/注意事項:
  - 既存の完了済みタスク成果物を全面再生成しない。
  - 現在のタスク範囲外の大規模リファクタリングを行わない。
  - root entrypoint、設定、DB初期化方式を理由なく破壊しない。
  - 要件にない外部システム、DB、Web、画像出力を勝手に追加しない。
  - allowed_filesにないファイルを修正する場合はsummaryに理由を書く。

### T03 認証・セッション・ユーザー入口

- 目的: 登録、ログイン、ログアウト、セッション維持、認証前後の画面遷移を実装する。Issueで明示がない場合も、GET / は単なるランディングページにせず、未認証なら /login、認証済みなら /menu へリダイレクトする。認証系の異常入力は 400/401/403/409/422 等の適切なHTTPステータスと対応するエラー画面で扱う。
- 依存: T01, T02
- 主な作成・修正対象:
  - `src/point_integrate_system/app.py`
  - `src/point_integrate_system/routes.py`
  - `src/point_integrate_system/services.py`
  - `src/point_integrate_system/validators.py`
  - `src/point_integrate_system/forms.py`
  - `src/point_integrate_system/errors.py`
  - `src/point_integrate_system/templates/base.html`
  - `src/point_integrate_system/templates/auth.html`
  - `src/point_integrate_system/templates/register.html`
  - `src/point_integrate_system/templates/menu.html`
  - `src/point_integrate_system/templates/error.html`
  - `src/point_integrate_system/static/css/style.css`
  - `src/point_integrate_system/static/js/main.js`
  - `tests/run_XXX/test_auth.py`
- 完了条件:
  - 登録・ログイン・ログアウトがFlask test clientで通る。
  - セッション制御が機能する。
  - GET / は未認証時 /login、認証済み時 /menu へリダイレクトする。
  - 認証・登録の異常系は通常のフォーム200再表示ではなく、適切な4xx/401/403/409/422系ステータスとエラー画面で処理する。
  - 各画面のURL・遷移先・概要は screen_flow_design と一致する。
- 禁止/注意事項:
  - 既存の完了済みタスク成果物を全面再生成しない。
  - 現在のタスク範囲外の大規模リファクタリングを行わない。
  - root entrypoint、設定、DB初期化方式を理由なく破壊しない。
  - 要件にない外部システム、DB、Web、画像出力を勝手に追加しない。
  - allowed_filesにないファイルを修正する場合はsummaryに理由を書く。

### T04 主要業務ワークフロー

- 目的: 要件の中核となる業務ロジック、状態更新、計算、一覧/詳細表示を実装する。
- 依存: T01, T02, T03
- 主な作成・修正対象:
  - `src/point_integrate_system/routes.py`
  - `src/point_integrate_system/services.py`
  - `src/point_integrate_system/repositories.py`
  - `src/point_integrate_system/errors.py`
  - `src/point_integrate_system/validators.py`
  - `src/point_integrate_system/templates/menu.html`
  - `src/point_integrate_system/templates/list.html`
  - `src/point_integrate_system/templates/detail.html`
  - `src/point_integrate_system/templates/form.html`
  - `tests/run_XXX/test_domain_workflows.py`
- 完了条件:
  - 主要業務フローがservice層で実装される。
  - 主要画面から業務操作できる。
  - Serviceはdatabase_schema_designのモデル名・フィールド名・constructor_fieldsから逸脱しない。
  - import/exportはmodule_contract_designと一致し、未定義シンボルをimportしない。
- 禁止/注意事項:
  - 既存の完了済みタスク成果物を全面再生成しない。
  - 現在のタスク範囲外の大規模リファクタリングを行わない。
  - root entrypoint、設定、DB初期化方式を理由なく破壊しない。
  - 要件にない外部システム、DB、Web、画像出力を勝手に追加しない。
  - allowed_filesにないファイルを修正する場合はsummaryに理由を書く。

### T05 通知・外部通信境界

- 目的: メール送信、通知、デバッグモード時の疑似送信、非デバッグ時の実送信境界を実装する。
- 依存: T01, T02, T03, T04
- 主な作成・修正対象:
  - `src/point_integrate_system/mail_service.py`
  - `src/point_integrate_system/services.py`
  - `src/point_integrate_system/routes.py`
  - `src/point_integrate_system/config.py`
  - `tests/run_XXX/test_mail_service.py`
- 完了条件:
  - デバッグ時は疑似送信できる。
  - 非デバッグ時の実送信関数がmock可能である。
- 禁止/注意事項:
  - 既存の完了済みタスク成果物を全面再生成しない。
  - 現在のタスク範囲外の大規模リファクタリングを行わない。
  - root entrypoint、設定、DB初期化方式を理由なく破壊しない。
  - 要件にない外部システム、DB、Web、画像出力を勝手に追加しない。
  - allowed_filesにないファイルを修正する場合はsummaryに理由を書く。

### T06 グループ・共有状態管理

- 目的: 複数ユーザーまたは複数要素のグループ化、共有状態、統合処理を実装する。
- 依存: T01, T02, T03, T04
- 主な作成・修正対象:
  - `src/point_integrate_system/services.py`
  - `src/point_integrate_system/repositories.py`
  - `src/point_integrate_system/models.py`
  - `src/point_integrate_system/routes.py`
  - `src/point_integrate_system/templates/group.html`
  - `src/point_integrate_system/templates/family.html`
  - `tests/run_XXX/test_grouping.py`
  - `tests/run_XXX/test_family.py`
- 完了条件:
  - グループ作成・追加・共有状態更新が動作する。
- 禁止/注意事項:
  - 既存の完了済みタスク成果物を全面再生成しない。
  - 現在のタスク範囲外の大規模リファクタリングを行わない。
  - root entrypoint、設定、DB初期化方式を理由なく破壊しない。
  - 要件にない外部システム、DB、Web、画像出力を勝手に追加しない。
  - allowed_filesにないファイルを修正する場合はsummaryに理由を書く。

### T07 画面・静的ファイル・画面仕様書

- 目的: HTML/CSS/JavaScriptとdisplay_difinition.mdを整備する。
- 依存: T01, T04
- 主な作成・修正対象:
  - `src/point_integrate_system/templates/*.html`
  - `src/point_integrate_system/static/css/style.css`
  - `src/point_integrate_system/static/js/main.js`
  - `reports/run_XXX/display_difinition.md`
  - `tests/run_XXX/test_templates.py`
  - `tests/run_XXX/test_static_assets.py`
  - `tests/run_XXX/test_display_definition.py`
- 完了条件:
  - 主要画面が存在する。
  - CSS/JS参照が整合する。
  - display_difinition.mdが成果物と一致する。
- 禁止/注意事項:
  - 既存の完了済みタスク成果物を全面再生成しない。
  - 現在のタスク範囲外の大規模リファクタリングを行わない。
  - root entrypoint、設定、DB初期化方式を理由なく破壊しない。
  - 要件にない外部システム、DB、Web、画像出力を勝手に追加しない。
  - allowed_filesにないファイルを修正する場合はsummaryに理由を書く。

### T08 JSON/XMLインターフェース

- 目的: JSON/XMLシリアライズ、サンプルデータ、interface_difinition.mdを実装する。
- 依存: T01, T04
- 主な作成・修正対象:
  - `src/point_integrate_system/serializers.py`
  - `data/exchange/*.json`
  - `data/exchange/*.xml`
  - `reports/run_XXX/interface_difinition.md`
  - `tests/run_XXX/test_serializers.py`
  - `tests/run_XXX/test_interface_definition.py`
- 完了条件:
  - serialize/deserializeが通る。
  - interface_difinition.mdが実装と整合する。
- 禁止/注意事項:
  - 既存の完了済みタスク成果物を全面再生成しない。
  - 現在のタスク範囲外の大規模リファクタリングを行わない。
  - root entrypoint、設定、DB初期化方式を理由なく破壊しない。
  - 要件にない外部システム、DB、Web、画像出力を勝手に追加しない。
  - allowed_filesにないファイルを修正する場合はsummaryに理由を書く。

### T09 全体結合・README・最終補強

- 目的: 全体のimport、起動、代表フロー、README、テスト整合を補強する。
- 依存: T01, T02, T03, T04, T05, T06, T07, T08
- 主な作成・修正対象:
  - `README.md`
  - `requirements.txt`
  - `pyproject.toml`
  - `app.py`
  - `src/app.py`
  - `src/point_integrate_system/**/*.py`
  - `tests/run_XXX/test_integration_flows.py`
- 完了条件:
  - 代表フローが結合試験で通る。
  - READMEに起動・試験・設計概要がある。
- 禁止/注意事項:
  - 既存の完了済みタスク成果物を全面再生成しない。
  - 現在のタスク範囲外の大規模リファクタリングを行わない。
  - root entrypoint、設定、DB初期化方式を理由なく破壊しない。
  - 要件にない外部システム、DB、Web、画像出力を勝手に追加しない。
  - allowed_filesにないファイルを修正する場合はsummaryに理由を書く。

## 6. 試験タスク分割

| 試験ID | 対応製造タスク | 試験名 | 優先度 | 試験ファイル |
|---|---|---|---|---|
| `TT01` | `T01` | Flask基盤・起動構成 の局所試験 | high | `tests/run_XXX/test_app_factory.py` |
| `TT02` | `T02` | 永続化モデル・Repository の局所試験 | high | `tests/run_XXX/test_models.py`, `tests/run_XXX/test_repositories.py` |
| `TT03` | `T03` | 認証・セッション・ユーザー入口 の局所試験 | high | `tests/run_XXX/test_auth.py` |
| `TT04` | `T04` | 主要業務ワークフロー の局所試験 | high | `tests/run_XXX/test_domain_workflows.py` |
| `TT05` | `T05` | 通知・外部通信境界 の局所試験 | high | `tests/run_XXX/test_mail_service.py` |
| `TT06` | `T06` | グループ・共有状態管理 の局所試験 | high | `tests/run_XXX/test_grouping.py`, `tests/run_XXX/test_family.py` |
| `TT07` | `T07` | 画面・静的ファイル・画面仕様書 の局所試験 | high | `tests/run_XXX/test_templates.py`, `tests/run_XXX/test_static_assets.py`, `tests/run_XXX/test_display_definition.py` |
| `TT08` | `T08` | JSON/XMLインターフェース の局所試験 | high | `tests/run_XXX/test_serializers.py`, `tests/run_XXX/test_interface_definition.py` |
| `TT09` | `T09` | 全体結合・README・最終補強 の局所試験 | high | `tests/run_XXX/test_integration_flows.py` |

## 7. 最終結合試験

- 起動性確認
- 主要正常系フロー
- 主要異常系フロー
- README/利用手順確認
- 主要URL確認
- template描画確認
- static CSS/JS参照確認
- display_difinition.md整合
- DBモデルと永続化の結合確認
- 認証・セッション代表フロー
- 通知/メール送信境界の確認
- JSON/XML roundtripとinterface_difinition.md整合
