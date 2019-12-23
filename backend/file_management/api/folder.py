# coding=utf-8
import logging
import flask_restplus
from flask import request

__author__ = 'LongHB'

from file_management import services
from file_management.api.schema import requests
from file_management.extensions import Namespace
from file_management.helpers.transformer import format_details_args

_logger = logging.getLogger(__name__)

ns = Namespace('folder', description='Folder operations')

_folder_details_req = ns.model('folder details', requests.folder_details_req)
_folder_create_req = ns.model('folder create', requests.folder_create_req)


@ns.route('/details', methods=['POST'])
class GetFolders(flask_restplus.Resource):
    @ns.expect(_folder_details_req, validate=True)
    def post(self):
        args = request.args or request.json
        format_details_args(args)
        return services.folder.folder_details(args)



@ns.route('/create', methods=['POST'])
class CreateFolder(flask_restplus.Resource):
    @ns.expect(_folder_create_req, validate=True)
    def post(self):
        args = request.args or request.json
        if not args:
            args = {}
        return services.folder.create_folder(args)
