from file_management.models import db, TimestampMixin
from file_management.constant import link

class File_info(db.Model, TimestampMixin):
    __tablename__ = 'file'

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    file_id = db.Column(db.String(100), primary_key=True)
    file_title = db.Column(db.String(256), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    parent_id = db.Column(db.String(100), nullable=False)
    db.column   
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    starred = db.Column(db.Boolean, nullable=False, default=False)
    trashed = db.Column(db.Boolean, nullable=False, default=False)
    trashed_time = db.Column(db.TIMESTAMP, nullable=True)
    version = db.Column(db.Integer, nullable=False, default = 1)
    has_thumbnail = db.Column(db.Boolean, nullable=False, default=False)
    thumbnail_url = db.Column(db.String(256), nullable=True, default=link.DEFAULT_THUMBNAIL)
    shared = db.Column(db.Boolean, nullable=False, default=False)
    
    
    def to_dict(self):
        return {
            'file_id': self.file_id,
            'file_title': self.file_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'file_size' : self.file_size,
            'parent_id': self.parent_id,
            'user_id' : self.user_id,
            'mime_type' : self.mime_type,
            'starred' : self.starred,
            'trashed' : self.trashed,
            'trashed_time' : self.trashed_time,
            'version' : self.version,
            'has_thumbnail' : self.has_thumbnail,
            'thumbnail_url' : self.thumbnail_url,
            'shared' : self.shared
        }

    def to_display_dict(self):
        return {
            'file_id': self.file_id,
            'file_title': self.file_name,
            'created_at': self.created_at,
            'file_size' : self.file_size,
            'parent_id': self.parent_id,
            'user_id' : self.user_id,
            'mime_type' : self.mime_type,
            'starred' : self.starred,
            'trashed' : self.trashed,
            'trashed_time' : self.trashed_time,
            'version' : self.version,
            'has_thumbnail' : self.has_thumbnail,
            'thumbnail_url' : self.thumbnail_url,
            'shared' : self.shared
        }
