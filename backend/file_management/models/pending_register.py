from file_management.models import db, TimestampMixin


class Pending_register(db.Model, TimestampMixin):
    __tablename__ = 'pending_registers'

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    username = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    fullname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(256))

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'fullname': self.fullname,
            'password': self.password,
            'created_at': self.created_at,
        }

    def to_display_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'fullname': self.fullname,
        }
