# coding=utf-8
from flask_restplus import fields


class ReqSchema:
    register_user_req = {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'fullname': fields.String(required=True, description='fullname of user'),
        'password': fields.String(required=True, description='user password'),
    }