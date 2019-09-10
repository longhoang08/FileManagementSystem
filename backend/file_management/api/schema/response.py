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