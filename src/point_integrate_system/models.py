from __future__ import annotations

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


# アプリ全体で共有する唯一のSQLAlchemy拡張インスタンスです。
db = SQLAlchemy()


class TimestampMixin:
    '''created_at / updated_at を持つモデル用の共通Mixinです。'''

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class User(TimestampMixin, db.Model):
    '''認証・セッションの主体ユーザーを表します。'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    point_account = db.relationship('PointAccount', back_populates='user', uselist=False)
    point_transactions = db.relationship('PointTransaction', back_populates='user')
    coupons = db.relationship('Coupon', back_populates='user')
    ranks = db.relationship('Rank', back_populates='user')
    orders = db.relationship('Order', back_populates='user')
    payments = db.relationship('Payment', back_populates='user')
    notifications = db.relationship('Notification', back_populates='user')
    owned_groups = db.relationship('UserGroup', back_populates='owner')

    def __repr__(self) -> str:
        return f'<User id={self.id!r} email={self.email!r}>'


class PointAccount(TimestampMixin, db.Model):
    '''ポイント残高・アカウント状態を表します。'''

    __tablename__ = 'point_accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    balance = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(32), nullable=False, default='active')

    user = db.relationship('User', back_populates='point_account')

    def __repr__(self) -> str:
        return f'<PointAccount id={self.id!r} user_id={self.user_id!r} balance={self.balance!r}>'


class PointTransaction(db.Model):
    '''ポイント増減・履歴を表します。'''

    __tablename__ = 'point_transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    point_delta = db.Column(db.Integer, nullable=False)
    transaction_type = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', back_populates='point_transactions')

    def __repr__(self) -> str:
        return f'<PointTransaction id={self.id!r} user_id={self.user_id!r} delta={self.point_delta!r}>'


class Coupon(TimestampMixin, db.Model):
    '''クーポン・特典を表します。'''

    __tablename__ = 'coupons'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(160), nullable=False)
    status = db.Column(db.String(32), nullable=False, default='active')
    description = db.Column(db.Text, nullable=True)

    user = db.relationship('User', back_populates='coupons')

    def __repr__(self) -> str:
        return f'<Coupon id={self.id!r} user_id={self.user_id!r} title={self.title!r}>'


class Rank(TimestampMixin, db.Model):
    '''ランク・会員グレードを表します。'''

    __tablename__ = 'ranks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(160), nullable=False)
    status = db.Column(db.String(32), nullable=False, default='active')
    description = db.Column(db.Text, nullable=True)

    user = db.relationship('User', back_populates='ranks')

    def __repr__(self) -> str:
        return f'<Rank id={self.id!r} user_id={self.user_id!r} title={self.title!r}>'


class Order(TimestampMixin, db.Model):
    '''注文・申請・依頼を表します。'''

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(160), nullable=False)
    status = db.Column(db.String(32), nullable=False, default='active')
    description = db.Column(db.Text, nullable=True)

    user = db.relationship('User', back_populates='orders')

    def __repr__(self) -> str:
        return f'<Order id={self.id!r} user_id={self.user_id!r} title={self.title!r}>'


class Payment(TimestampMixin, db.Model):
    '''支払い・決済を表します。'''

    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(160), nullable=False)
    status = db.Column(db.String(32), nullable=False, default='active')
    description = db.Column(db.Text, nullable=True)

    user = db.relationship('User', back_populates='payments')

    def __repr__(self) -> str:
        return f'<Payment id={self.id!r} user_id={self.user_id!r} title={self.title!r}>'


class Notification(db.Model):
    '''通知を表します。'''

    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    event_type = db.Column(db.String(64), nullable=False)
    payload_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', back_populates='notifications')

    def __repr__(self) -> str:
        return f'<Notification id={self.id!r} user_id={self.user_id!r} event_type={self.event_type!r}>'


class UserGroup(db.Model):
    '''共有・グループ状態を表します。'''

    __tablename__ = 'user_groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    owner_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    owner = db.relationship('User', back_populates='owned_groups')

    def __repr__(self) -> str:
        return f'<UserGroup id={self.id!r} owner_user_id={self.owner_user_id!r} name={self.name!r}>'


__all__ = [
    'db',
    'User',
    'PointAccount',
    'PointTransaction',
    'Coupon',
    'Rank',
    'Order',
    'Payment',
    'Notification',
    'UserGroup',
]
