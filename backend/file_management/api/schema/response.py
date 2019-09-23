# coding=utf-8
from flask_restplus import fields


class ResSchema:
    user_res = {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'fullname': fields.String(required=True, description='fullname of user'),
        'avatar_url': fields.String(required=True, description='avatar url of user'),
    }

    pending_register_res = {
        'username': fields.String(required=True, description="Username"),
        'email': fields.String(required=True, description="Email"),
        'fullname': fields.String(required=True, description="User full name"),
    }

    @classmethod
    def make_logs_res(self, ns):
        log_field = ns.model('log', {
            'message' : fields.String(required=True, description="Message"),
            'created_at': fields.DateTime(required=True, description="Create at")
        })

        logs_res = {
            'logs': fields.List(fields.Nested(log_field))
        }
        return logs_res

    @classmethod
    def make_notification_res(self, ns):
        notification_field = ns.model('notification', {
            'message' : fields.String(required=True, description="Message"),
            'created_at': fields.DateTime(required=True, description="Create at")
        })

        notification_res = {
            'notifications' : fields.List(fields.Nested(notification_field))
        }
        return notification_res

    