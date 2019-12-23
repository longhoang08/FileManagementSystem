from datetime import datetime

from file_management.models import db, TimestampMixin


class Notification(db.Model, TimestampMixin):
    __tablename__ = 'notifications'

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    viewed = db.Column(db.Boolean, nullable=False)
    owner = db.Column(db.Integer, nullable=False)
    file_id = db.Column(db.String(512), nullable=False)

    def to_dict(self):
        from file_management.repositories.files import utils
        from file_management.repositories.user import find_one_by_user_id
        file = utils.get_file(self.file_id)
        if not file:
            return None
        owner = find_one_by_user_id(self.owner)
        return {
            'id': self.id,
            'viewed': self.viewed,
            'file_id': self.file_id,
            'file_title': file.get('file_title'),
            'file_type': file.get('file_type'),
            'owner': {
                'id': self.owner,
                'avatar_url': owner.avatar_url,
                'fullname': owner.fullname
            },
            'created_at': datetime.timestamp(self.created_at),
        }
