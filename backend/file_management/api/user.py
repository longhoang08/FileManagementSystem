# coding=utf-8
import logging

import flask_restplus
from flask import request, jsonify

from file_management import services, models, repositories
from file_management.extensions import Namespace
from file_management.extensions.custom_exception import InvalidLoginTokenException
from file_management.helpers import get_max_age
from .schema.response import ResSchema
from .schema.request import ReqSchema

__author__ = 'longhb'
_logger = logging.getLogger(__name__)

ns = Namespace('users', description='User operations')

_user_res = ns.model('user_res', ResSchema.user_res)


@ns.route('/get_status', methods=['GET'])
class UserStatus(flask_restplus.Resource):
    @ns.marshal_with(_user_res)
    def get(self):
        "fetch user status by checking jwt token"
        from file_management.constant.user import Constant_user
        try:
            email = services.token.check_jwt_token()
        except:
            raise InvalidLoginTokenException()
        if (email == None):
            return Constant_user.none_user
        user = services.user.fetch_user_status_by_email(email)
        return user


_login_req = ns.model('login_req', ReqSchema.login_req)


@ns.marshal_with(_user_res)
@ns.route('/login', methods=['GET', 'POST'])
class Login(flask_restplus.Resource):
    @ns.expect(_login_req, validate=True)
    def post(self):
        data = request.args or request.json
        resp = services.user.login(**data)
        return resp


@ns.route('/logout', methods=['GET', 'POST'])
class Logout(flask_restplus.Resource):
    def post(self):
        resp = services.user.logout()
        return resp