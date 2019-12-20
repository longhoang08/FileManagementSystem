"""
Just a test api
You should remove this files after fully understand my code base!
"""
# coding=utf-8
import logging

import flask_restplus
from flask import request

from file_management import services
from file_management.api.schema import requests
from file_management.repositories import files
from file_management.extensions import Namespace

__author__ = 'jian'
_logger = logging.getLogger(__name__)

ns = Namespace('files', description='File operations')


@ns.route('/insert', methods=['POST'])
class InsertFiles(flask_restplus.Resource):
    def post(selfs):
        args = request.args or request.json
        if not args:
            args = {}
        res = files.insert.insert(**args)
        return res


@ns.route('/delete', methods=['GET'])
class DeleteFiles(flask_restplus.Resource):
    def get(self):
        args = request.args or request.json
        if not args:
            args = {}
        res = files.delete.delete(**args)
        return res


@ns.route('/update', methods=['POST'])
class UpdateFiles(flask_restplus.Resource):
    def post(self):
        args = request.args or request.json
        if not args:
            args = {}
        res = files.update.update(**args)
        return res


_file_details_req = ns.model('file_details_request', requests.file_details_req)


@ns.route('/details', methods=['POST'])
class GetFiles(flask_restplus.Resource):
    @ns.expect(_file_details_req, validate=True)
    def post(self):
        args = request.args or request.json
        if not args:
            args = {}
        return services.file.search(args)
