from file_management.models import db, TimestampMixin


class File_info(db.Model, TimestampMixin):
    __tablename__ = 'file'

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    file_id = db.Column(db.String(30), primary_key=True)
    file_title = db.Column(db.String(256), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    modified_at = db.Column(db.DateTime(False), nullable=False)
    parent_id = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    # db.column
    # user_id = db.Column(db.Integer, db.ForeignKey('user_id'),nullable=False)

    def to_dict(self):
        return {
            'file_id': self.file_id,
            'file_title': self.file_name,
            'created_at': self.created_at,
            'file_size' : self.file_size,
            'modified_at': self.modified_at,
            'parent_id': self.parent_id,
            'user_id' : self.user_id
        }

    def to_display_dict(self):
        return {
            'file_title': self.file_name,
            'created_at': self.created_at,
            'user_id': self.user_id,
        }
