# coding=utf-8
import logging

from flask_restplus import Resource, reqparse, fields
from flask import request

from file_management import services
from file_management.extensions import Namespace
from file_management.services.admin import get_all_users, search_users, block_user, \
    un_block_user
from file_management.helpers.check_role import admin_required
from . import requests, responses

__author__ = 'Dat'
_logger = logging.getLogger(__name__)

ns = Namespace('admin', description='Admin operations')

_user_res = ns.model('user_response', responses.user_res)
_users_list_res = ns.model('users list response', {
    'users': fields.List(fields.Nested(_user_res))
})

_search_users_parser = reqparse.RequestParser()
_search_users_parser.add_argument('username')
_search_users_parser.add_argument('page', type=int)
_search_users_parser.add_argument('ipp', type=int)


@ns.route('/search_users', methods=['GET'])
class SearchUsers(Resource):
    @admin_required
    @ns.expect(_search_users_parser)
    @ns.marshal_with(_users_list_res)
    def get(self):
        """
        Search user by username
        """
        users = search_users(**request.args)
        return {
            "users": users
        }


_switch_block_user_req = ns.model('Block-Unlock Request', requests.switch_block_user_req)


@ns.route('/block_user', methods=['POST'])
class BlockUser(Resource):
    @ns.expect(_switch_block_user_req, validate=True)
    @admin_required
    @ns.marshal_with(_user_res)
    def post(self):
        """
        Block user by email
        """
        email = request.json['email']
        user = block_user(email)
        return user


@ns.route('/un_block_user', methods=['POST'])
class UnBlockUser(Resource):
    @ns.expect(_switch_block_user_req, validate=True)
    @admin_required
    @ns.marshal_with(_user_res)
    def post(self):
        """
        Un Block user by email
        """
        email = request.json['email']
        user = un_block_user(email)
        return user
