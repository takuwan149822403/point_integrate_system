import pytest

from point_integrate_system.app import create_app
from point_integrate_system.models import PointAccount, PointTransaction, User, db
from point_integrate_system.repositories import (
    PointAccountRepository,
    PointTransactionRepository,
    RepositoryError,
    UserRepository,
)


@pytest.fixture()
def app():
    '''試験区分: 正常系
    確認項目: Repository試験用のDBを初期化できること。
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


def test_user_repository_create_find_update_delete(app):
    '''試験区分: 正常系
    確認項目: UserRepositoryで作成・検索・更新・削除ができること。
    '''
    repository = UserRepository()

    user = repository.create(
        name='Repository利用者',
        email='repo@example.com',
        password_hash='hash',
        is_active=True,
    )

    assert user.id is not None
    assert repository.get_by_id(user.id).email == 'repo@example.com'
    assert repository.find_by_email('repo@example.com').name == 'Repository利用者'

    repository.update(user, name='更新済み利用者')
    assert repository.get_by_id(user.id).name == '更新済み利用者'

    repository.delete(user)
    assert repository.get_by_id(user.id) is None


def test_point_repositories_save_and_search_by_user(app):
    '''試験区分: 正常系
    確認項目: ポイント関連Repositoryで保存・ユーザー別検索ができること。
    '''
    user = UserRepository().create(
        name='ポイント利用者',
        email='point@example.com',
        password_hash='hash',
    )
    account_repository = PointAccountRepository()
    transaction_repository = PointTransactionRepository()

    account = account_repository.create(user_id=user.id, balance=500, status='active')
    transaction = transaction_repository.create(
        user_id=user.id,
        point_delta=500,
        transaction_type='add',
        description='テスト付与',
    )

    assert isinstance(account, PointAccount)
    assert account_repository.find_by_user_id(user.id).balance == 500
    assert isinstance(transaction, PointTransaction)
    assert transaction_repository.list_by_user_id(user.id)[0].description == 'テスト付与'


def test_repository_rolls_back_on_integrity_error(app):
    '''試験区分: 異常系
    確認項目: 一意制約違反時にRepositoryErrorとなり、rollback後に後続保存できること。
    '''
    repository = UserRepository()
    repository.create(name='重複1', email='duplicate@example.com', password_hash='hash')

    with pytest.raises(RepositoryError):
        repository.create(name='重複2', email='duplicate@example.com', password_hash='hash')

    recovered = repository.create(name='復旧確認', email='recovered@example.com', password_hash='hash')
    assert recovered.id is not None
    assert repository.find_by_email('recovered@example.com') is not None


def test_repository_rejects_unknown_update_field(app):
    '''試験区分: 異常系
    確認項目: 存在しないモデル属性を更新しようとするとRepositoryErrorになること。
    '''
    repository = UserRepository()
    user = repository.create(name='属性確認', email='field@example.com', password_hash='hash')

    with pytest.raises(RepositoryError):
        repository.update(user, unknown_field='invalid')
