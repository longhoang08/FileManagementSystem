from file_management.models import db, TimestampMixin


class Notification(db.Model, TimestampMixin):
    __tablename__ = 'notifications'

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False, db.ForeignKey('users.id'))
    message = db.Column(db.String(512), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'message': self.message,
        }