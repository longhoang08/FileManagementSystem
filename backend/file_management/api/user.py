# coding=utf-8
import logging

import flask_restplus
from flask import request

from file_management import services
from file_management.extensions import Namespace
from file_management.extensions.custom_exception import InvalidLoginTokenException
from . import responses, requests

__author__ = 'longhb'

from ..services.user import get_details_by_ids

_logger = logging.getLogger(__name__)

ns = Namespace('users', description='User operations')

_user_res = ns.model('user_res', responses.user_res)


@ns.route('/get_status', methods=['GET'])
class UserStatus(flask_restplus.Resource):
    # @ns.marshal_with(_user_res)
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


_login_req = ns.model('login_req', requests.login_req)


@ns.route('/login', methods=['GET', 'POST'])
class Login(flask_restplus.Resource):
    @ns.expect(_login_req, validate=True)
    # @ns.marshal_with(_user_res)
    def post(self):
        "check username and password and set jwt token to httponly cookies"
        data = request.args or request.json
        resp = services.user.login(**data)
        return resp


@ns.route('/logout', methods=['GET', 'POST'])
class Logout(flask_restplus.Resource):
    def post(self):
        "remove jwt token from httponly cookies"
        resp = services.user.logout()
        return resp


_user_details_req = ns.model('user_details_req', requests.user_details_req)


@ns.route('/info', methods=['POST'])
class GetUserInfo(flask_restplus.Resource):
    @ns.expect(_user_details_req, validate=True)
    def post(self):
        args = request.args or request.json
        return get_details_by_ids(args.get('ids'))
