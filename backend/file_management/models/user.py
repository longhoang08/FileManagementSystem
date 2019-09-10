# coding=utf-8
import datetime

from file_management.constant import link
from file_management.models import db, TimestampMixin


class User(db.Model, TimestampMixin):
    """
    Contains information of users table
    """
    __tablename__ = 'users'

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    fullname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(256))
    avatar_url = db.Column(db.String(256), default=link.DEFAULT_AVATAR)

    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    last_login = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.now)
    un_block_at = db.Column(db.TIMESTAMP, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'fullname': self.fullname,
            'avatarUrl': self.avatar_url,
            'isAdmin': self.is_admin,
            'isActive': self.is_active,
            'password': self.password,
        }

    def to_display_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'fullname': self.fullname,
            'avatar_url': self.avatar_url,
        }
