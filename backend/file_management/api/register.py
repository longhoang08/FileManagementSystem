# coding=utf-8
import logging
import os
import flask_restplus
from flask import request, redirect

from file_management import services
from file_management.extensions import Namespace
from file_management.helpers import decode_token
from file_management.services.pending_register import send_confirm_email
from file_management.repositories.files import insert, utils

# from file_management.api import requests, responses
from . import requests, responses

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)

ns = Namespace('register', description='Register operations')

_register_req = ns.model('register_req', requests.register_user_req)
_register_res = ns.model('register_res', responses.pending_register_res)


@ns.route('/', methods=['GET', 'POST'])
class Registers(flask_restplus.Resource):
    @ns.expect(_register_req, validate=True)
    @ns.marshal_with(_register_res)
    def post(self):
        "validate register data, add data to pending register table and send confirm email"
        data = request.args or request.json
        pending_register = services.pending_register.create_pending_register(
            **data)
        send_confirm_email(**data)
        return pending_register


@ns.route('/confirm_email/<token>', methods=['GET'])
class Confirm_email(flask_restplus.Resource):

    def get(self, token):
        "checking jwt token in param and add new user to user table"
        email = decode_token(token)
        user = services.user.confirm_user_by_email(email)

        user_inf = user.to_display_dict()
        user_id = user_inf['user_id']
        # create home
        insert.insert(str(user_id), "home", 0, "0", str(user_id), "folder", "", "")
        folders = utils.get_ancestors(str(user_id))
        path_upload = '/'.join(folders)
        if not os.path.exists(path_upload):
            os.makedirs(path_upload)
        return redirect("http://ufile.ml")
