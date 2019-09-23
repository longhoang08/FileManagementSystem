import logging

from file_management.models import db, TimestampMixin


class Log(db.Model, TimestampMixin):
    __tablename__ = 'logs'

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(512), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'message': self.message,
        }