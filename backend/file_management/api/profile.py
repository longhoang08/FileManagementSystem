# coding=utf-8
import logging

import flask_restplus
from flask import request

from file_management import services
from file_management.extensions import Namespace
from file_management.services.user import check_permission
from . import requests, responses

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)

ns = Namespace('profile', description='Profile operations')

_change_req = ns.model('change_password_req', requests.change_password_req)
_change_res = ns.model('change_password_res', responses.user_res)


@ns.route('/change_password', methods=['GET', 'POST'])
class Change_password(flask_restplus.Resource):
    @ns.expect(_change_req, validate=True)
    @ns.marshal_with(_change_res)
    def post(self):
        "validate user by current password and jwt token and set new password"
        data = request.args or request.json
        email = data.get('email')
        check_permission(email)
        new_user = services.password.change_password(**data)
        return new_user
