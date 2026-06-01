import pytest

from point_integrate_system.app import create_app
from point_integrate_system.models import db
from point_integrate_system.repositories import (
    CouponRepository,
    NotificationRepository,
    OrderRepository,
    PaymentRepository,
    PointAccountRepository,
    PointTransactionRepository,
    RankRepository,
    RepositoryError,
    UserGroupRepository,
    UserRepository,
)


@pytest.fixture()
def app():
    """試験区分: 正常系
    確認項目: Repository試験用のDB初期化が成功すること
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


def test_user_repository_create_get_and_find_by_email(app):
    """試験区分: 正常系
    確認項目: UserRepositoryで作成・主キー検索・メール検索ができること
    """
    with app.app_context():
        repo = UserRepository()
        user = repo.create(
            name="田中一郎",
            email="ichiro@example.com",
            password_hash="hash",
            is_active=True,
        )

        assert user.id is not None
        assert repo.get_by_id(user.id).email == "ichiro@example.com"
        assert repo.find_by_email(" ICHIRO@example.com ").id == user.id
        assert repo.find_by_email(" ") is None


def test_point_account_repository_create_and_get_by_user_id(app):
    """試験区分: 正常系
    確認項目: PointAccountRepositoryでポイント口座を保存・検索できること
    """
    with app.app_context():
        user = UserRepository().create(
            name="鈴木次郎",
            email="jiro@example.com",
            password_hash="hash",
        )
        account_repo = PointAccountRepository()
        account = account_repo.create(user_id=user.id, balance=500, status="active")

        loaded = account_repo.get_by_user_id(user.id)

        assert loaded.id == account.id
        assert loaded.balance == 500
        assert account_repo.get_by_user_id(0) is None


def test_repositories_list_by_user_id_for_major_models(app):
    """試験区分: 正常系
    確認項目: 主要RepositoryでユーザーIDによる一覧検索ができること
    """
    with app.app_context():
        user = UserRepository().create(
            name="高橋三郎",
            email="saburo@example.com",
            password_hash="hash",
        )

        PointTransactionRepository().create(
            user_id=user.id,
            point_delta=100,
            transaction_type="add",
            description="付与",
        )
        CouponRepository().create(
            user_id=user.id,
            title="テストクーポン",
            status="active",
            description="説明",
        )
        RankRepository().create(
            user_id=user.id,
            title="シルバー",
            status="active",
            description="説明",
        )
        OrderRepository().create(
            user_id=user.id,
            title="交換申請",
            status="active",
            description="説明",
        )
        PaymentRepository().create(
            user_id=user.id,
            title="カード決済",
            status="active",
            description="説明",
        )
        NotificationRepository().create(
            user_id=user.id,
            event_type="coupon_created",
            payload_json='{"coupon": true}',
        )

        assert len(PointTransactionRepository().list_by_user_id(user.id)) == 1
        assert len(CouponRepository().list_by_user_id(user.id)) == 1
        assert len(RankRepository().list_by_user_id(user.id)) == 1
        assert len(OrderRepository().list_by_user_id(user.id)) == 1
        assert len(PaymentRepository().list_by_user_id(user.id)) == 1
        assert len(NotificationRepository().list_by_user_id(user.id)) == 1
        assert CouponRepository().list_by_user_id(0) == []


def test_user_group_repository_list_by_owner_user_id(app):
    """試験区分: 正常系
    確認項目: UserGroupRepositoryで所有者ユーザーID検索ができること
    """
    with app.app_context():
        user = UserRepository().create(
            name="伊藤四郎",
            email="shiro@example.com",
            password_hash="hash",
        )
        group_repo = UserGroupRepository()
        group = group_repo.create(name="共有グループ", owner_user_id=user.id)

        groups = group_repo.list_by_owner_user_id(user.id)

        assert len(groups) == 1
        assert groups[0].id == group.id
        assert group_repo.list_by_owner_user_id(-1) == []


def test_repository_rolls_back_and_raises_repository_error_on_commit_failure(app):
    """試験区分: 異常系
    確認項目: DBコミット失敗時にロールバックしRepositoryErrorを送出すること
    """
    with app.app_context():
        repo = UserRepository()
        repo.create(name="重複1", email="duplicate@example.com", password_hash="hash")

        with pytest.raises(RepositoryError):
            repo.create(name="重複2", email="duplicate@example.com", password_hash="hash")

        assert repo.find_by_email("duplicate@example.com") is not None
        assert len(repo.list_all()) == 1
