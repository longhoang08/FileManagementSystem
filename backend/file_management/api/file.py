"""
Just a test api
You should remove this file after fully understand my code base!
"""
# coding=utf-8
import logging

import flask_restplus
from flask import request

from file_management.services.file import insert, search, delete, update
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
        res = insert.insert(**args)
        return res


@ns.route('/search', methods=['POST'])
class SearchFiles(flask_restplus.Resource):
    def post(selfs):
        args = request.args or request.json
        if not args:
            args = {}
        res = search.search(**args)
        return res


@ns.route('/delete', methods=['GET'])
class DeleteFiles(flask_restplus.Resource):
    def get(self):
        args = request.args or request.json
        if not args:
            args = {}
        res = delete.delete(**args)
        return res


@ns.route('/update', methods=['POST'])
class UpdateFiles(flask_restplus.Resource):
    def post(self):
        args = request.args or request.json
        if not args:
            args = {}
        res = update.update(**args)
        return res
