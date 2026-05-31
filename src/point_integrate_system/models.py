"""永続化モデル定義。

T02ではFlask-SQLAlchemyの単一dbインスタンスと、設計契約で固定された
主要テーブルのモデルだけを定義する。
"""

from __future__ import annotations

from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def utc_now() -> datetime:
    """DB保存用のUTC現在時刻を返す。"""
    return datetime.now(timezone.utc)


class TimestampMixin:
    """created_at / updated_at を持つモデル用Mixin。"""

    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )


class User(db.Model, TimestampMixin):
    """認証・セッションの主体ユーザー。"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    point_accounts = db.relationship("PointAccount", backref="user", lazy=True)
    point_transactions = db.relationship("PointTransaction", backref="user", lazy=True)
    coupons = db.relationship("Coupon", backref="user", lazy=True)
    ranks = db.relationship("Rank", backref="user", lazy=True)
    orders = db.relationship("Order", backref="user", lazy=True)
    payments = db.relationship("Payment", backref="user", lazy=True)
    notifications = db.relationship("Notification", backref="user", lazy=True)
    owned_groups = db.relationship("UserGroup", backref="owner", lazy=True)

    def __repr__(self) -> str:
        return f"<User id={self.id!r} email={self.email!r}>"


class PointAccount(db.Model, TimestampMixin):
    """ポイント残高・アカウント状態。"""

    __tablename__ = "point_accounts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    balance = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(32), nullable=False, default="active")

    def __repr__(self) -> str:
        return f"<PointAccount id={self.id!r} user_id={self.user_id!r} balance={self.balance!r}>"


class PointTransaction(db.Model):
    """ポイント増減・履歴。"""

    __tablename__ = "point_transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    point_delta = db.Column(db.Integer, nullable=False)
    transaction_type = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)

    def __repr__(self) -> str:
        return (
            f"<PointTransaction id={self.id!r} user_id={self.user_id!r} "
            f"point_delta={self.point_delta!r}>"
        )


class Coupon(db.Model, TimestampMixin):
    """クーポン・特典。"""

    __tablename__ = "coupons"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(160), nullable=False)
    status = db.Column(db.String(32), nullable=False, default="active")
    description = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Coupon id={self.id!r} user_id={self.user_id!r} title={self.title!r}>"


class Rank(db.Model, TimestampMixin):
    """ランク・会員グレード。"""

    __tablename__ = "ranks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(160), nullable=False)
    status = db.Column(db.String(32), nullable=False, default="active")
    description = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Rank id={self.id!r} user_id={self.user_id!r} title={self.title!r}>"


class Order(db.Model, TimestampMixin):
    """注文・申請・依頼。"""

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(160), nullable=False)
    status = db.Column(db.String(32), nullable=False, default="active")
    description = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Order id={self.id!r} user_id={self.user_id!r} title={self.title!r}>"


class Payment(db.Model, TimestampMixin):
    """支払い・決済。"""

    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(160), nullable=False)
    status = db.Column(db.String(32), nullable=False, default="active")
    description = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Payment id={self.id!r} user_id={self.user_id!r} title={self.title!r}>"


class Notification(db.Model):
    """通知。"""

    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    event_type = db.Column(db.String(64), nullable=False)
    payload_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)

    def __repr__(self) -> str:
        return f"<Notification id={self.id!r} user_id={self.user_id!r} event_type={self.event_type!r}>"


class UserGroup(db.Model):
    """共有・グループ状態。"""

    __tablename__ = "user_groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    owner_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)

    def __repr__(self) -> str:
        return f"<UserGroup id={self.id!r} owner_user_id={self.owner_user_id!r} name={self.name!r}>"
