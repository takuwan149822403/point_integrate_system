import pytest

from point_integrate_system.app import create_app
from point_integrate_system.models import (
    Coupon,
    Notification,
    Order,
    Payment,
    PointAccount,
    PointTransaction,
    Rank,
    User,
    UserGroup,
    db,
)


@pytest.fixture()
def app():
    """試験区分: 正常系
    確認項目: テスト用アプリでDB初期化とテーブル作成ができること
    """
    flask_app = create_app("testing")
    flask_app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        TESTING=True,
    )
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


def test_db_initialization_creates_all_contract_tables(app):
    """試験区分: 正常系
    確認項目: 設計契約で定義された主要テーブルが作成されること
    """
    with app.app_context():
        table_names = set(db.metadata.tables.keys())

    assert {
        "users",
        "point_accounts",
        "point_transactions",
        "coupons",
        "ranks",
        "orders",
        "payments",
        "notifications",
        "user_groups",
    }.issubset(table_names)


def test_user_model_can_be_created_saved_and_loaded(app):
    """試験区分: 正常系
    確認項目: Userモデルを作成・保存・検索できること
    """
    with app.app_context():
        user = User(
            name="山田太郎",
            email="taro@example.com",
            password_hash="hashed-password",
            is_active=True,
        )
        db.session.add(user)
        db.session.commit()

        loaded = db.session.get(User, user.id)

    assert loaded is not None
    assert loaded.name == "山田太郎"
    assert loaded.email == "taro@example.com"
    assert loaded.password_hash == "hashed-password"
    assert loaded.is_active is True
    assert loaded.created_at is not None
    assert loaded.updated_at is not None


def test_related_models_can_be_created_saved_and_loaded(app):
    """試験区分: 正常系
    確認項目: 主要関連モデルを作成・保存・検索できること
    """
    with app.app_context():
        user = User(name="佐藤花子", email="hanako@example.com", password_hash="hash")
        db.session.add(user)
        db.session.commit()

        records = [
            PointAccount(user_id=user.id, balance=1200, status="active"),
            PointTransaction(
                user_id=user.id,
                point_delta=300,
                transaction_type="add",
                description="初回付与",
            ),
            Coupon(user_id=user.id, title="初回クーポン", status="active", description="説明"),
            Rank(user_id=user.id, title="ゴールド", status="active", description="説明"),
            Order(user_id=user.id, title="申請", status="active", description="説明"),
            Payment(user_id=user.id, title="決済", status="active", description="説明"),
            Notification(user_id=user.id, event_type="point_added", payload_json='{"point": 300}'),
            UserGroup(name="家族グループ", owner_user_id=user.id),
        ]
        db.session.add_all(records)
        db.session.commit()

        assert PointAccount.query.filter_by(user_id=user.id).one().balance == 1200
        assert PointTransaction.query.filter_by(user_id=user.id).one().point_delta == 300
        assert Coupon.query.filter_by(user_id=user.id).one().title == "初回クーポン"
        assert Rank.query.filter_by(user_id=user.id).one().title == "ゴールド"
        assert Order.query.filter_by(user_id=user.id).one().title == "申請"
        assert Payment.query.filter_by(user_id=user.id).one().title == "決済"
        assert Notification.query.filter_by(user_id=user.id).one().event_type == "point_added"
        assert UserGroup.query.filter_by(owner_user_id=user.id).one().name == "家族グループ"


def test_forbidden_alias_keyword_is_rejected_by_model_constructor(app):
    """試験区分: 異常系
    確認項目: 設計契約外の別名キーワードでモデルを生成できないこと
    """
    with app.app_context():
        with pytest.raises(TypeError):
            User(name="別名", mail="alias@example.com", password_hash="hash")
        with pytest.raises(TypeError):
            PointAccount(user_id=1, points=100)
        with pytest.raises(TypeError):
            PointTransaction(user_id=1, points=100, transaction_type="add")
