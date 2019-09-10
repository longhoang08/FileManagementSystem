# coding=utf-8
import logging

import flask_restplus
from flask import request

from file_management import services
from file_management.extensions import Namespace
from file_management.helpers import decode_token
from file_management.repositories import pending_register
from file_management.services import user
from file_management.services.pending_register import send_confirm_email
from .schema.request import ReqSchema
from .schema.response import ResSchema

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)

ns = Namespace('register', description='Register operations')

_register_req = ns.model('register_req', ReqSchema.register_user_req)
_register_res = ns.model('register_res', ResSchema.pending_register_res)


@ns.route('/', methods=['GET', 'POST'])
class Registers(flask_restplus.Resource):
    @ns.expect(_register_req, validate=True)
    @ns.marshal_with(_register_res)
    def post(self):
        data = request.args or request.json
        pending_register = services.pending_register.create_pending_register(**data)
        send_confirm_email(**data)
        return pending_register


@ns.route('/confirm_email/<token>', methods=['GET'])
class Confirm_email(flask_restplus.Resource):

    # create new user, delete pending register request and save password to historic password
    def get(self, token):
        email = decode_token(token)
        new_user = user.create_user_from_pending_register(email)
        pending_register.delete_one_by_email(email)
        return new_user.to_display_dict()
