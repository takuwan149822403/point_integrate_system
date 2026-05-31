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
    '''試験区分: 正常系
    確認項目: テスト用FlaskアプリでDBスキーマを作成・破棄できること。
    '''
    flask_app = create_app('testing')
    flask_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


def test_db_extension_is_initialized(app):
    '''試験区分: 正常系
    確認項目: create_app()後にSQLAlchemy拡張が初期化されていること。
    '''
    assert 'sqlalchemy' in app.extensions


def test_user_model_can_be_saved_and_found(app):
    '''試験区分: 正常系
    確認項目: Userモデルを作成・保存・検索できること。
    '''
    user = User(name='山田太郎', email='taro@example.com', password_hash='hashed-password')
    db.session.add(user)
    db.session.commit()

    found = User.query.filter_by(email='taro@example.com').first()

    assert found is not None
    assert found.id == user.id
    assert found.name == '山田太郎'
    assert found.is_active is True
    assert found.created_at is not None
    assert found.updated_at is not None


def test_major_models_can_be_created_saved_and_found(app):
    '''試験区分: 正常系
    確認項目: 主要モデルを作成・保存・検索できること。
    '''
    user = User(name='佐藤花子', email='hanako@example.com', password_hash='hash')
    db.session.add(user)
    db.session.flush()

    records = [
        PointAccount(user_id=user.id, balance=1200, status='active'),
        PointTransaction(user_id=user.id, point_delta=300, transaction_type='add', description='初回付与'),
        Coupon(user_id=user.id, title='ウェルカムクーポン', status='active', description='登録特典'),
        Rank(user_id=user.id, title='シルバー', status='active', description='会員ランク'),
        Order(user_id=user.id, title='ポイント交換申請', status='active', description='申請内容'),
        Payment(user_id=user.id, title='カード決済', status='active', description='決済内容'),
        Notification(user_id=user.id, event_type='point_added', payload_json='{ "point": 300 }'),
        UserGroup(name='家族グループ', owner_user_id=user.id),
    ]
    db.session.add_all(records)
    db.session.commit()

    assert PointAccount.query.filter_by(user_id=user.id).one().balance == 1200
    assert PointTransaction.query.filter_by(user_id=user.id).one().point_delta == 300
    assert Coupon.query.filter_by(user_id=user.id).one().title == 'ウェルカムクーポン'
    assert Rank.query.filter_by(user_id=user.id).one().title == 'シルバー'
    assert Order.query.filter_by(user_id=user.id).one().title == 'ポイント交換申請'
    assert Payment.query.filter_by(user_id=user.id).one().title == 'カード決済'
    assert Notification.query.filter_by(user_id=user.id).one().event_type == 'point_added'
    assert UserGroup.query.filter_by(owner_user_id=user.id).one().name == '家族グループ'


def test_forbidden_alias_keywords_are_not_accepted(app):
    '''試験区分: 異常系
    確認項目: 設計で禁止された別名キーワードではモデルを生成できないこと。
    '''
    with pytest.raises(TypeError):
        User(name='別名利用者', mail='alias@example.com', password_hash='hash')

    with pytest.raises(TypeError):
        PointAccount(user_id=1, points=100)

    with pytest.raises(TypeError):
        PointTransaction(user_id=1, points=100, transaction_type='add')
