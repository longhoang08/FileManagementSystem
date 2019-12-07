"""
Just a test api
You should remove this file after fully understand my code base!
"""
# coding=utf-8
import logging

import flask_restplus
from flask import request

from file_management import services
from file_management.extensions import Namespace

__author__ = 'longhb'
_logger = logging.getLogger(__name__)


ns = Namespace('files', description='File operations')

@ns.route('/allFile', methods=['GET'])
class AllFiles(flask_restplus.Resource):
    def get(selfs):
        "get all file"
        args = request.args or request.json
        if not args: args = {}
        files = services.file.get_all_files(args)
        return files