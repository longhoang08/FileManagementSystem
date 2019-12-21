# coding=utf-8
import logging

import flask_restplus
from flask import request

from file_management import services
from file_management.api.schema import requests
from file_management.repositories import files
from file_management.extensions import Namespace
from file_management.helpers.check_role import view_privilege_required, edit_privilege_required

__author__ = 'jian'
_logger = logging.getLogger(__name__)

ns = Namespace('files', description='File operations')

_file_details_req = ns.model('file_details_request', requests.file_details_req)


@ns.route('/details', methods=['POST'])
class GetFiles(flask_restplus.Resource):
    @ns.expect(_file_details_req, validate=True)
    def post(self):
        args = request.args or request.json
        if not args:
            args = {}
        return services.file.search(args)


_status_res = ns.model('Status Response', {
    "status": flask_restplus.fields.Boolean(required=True,
                                            description='Return status after remove, add star or files')})
_del_req = ns.model('Trash Request', requests.trash_req)


@ns.route('/temp_del', methods=['POST'])
class TemporaryDelete(flask_restplus.Resource):
    @ns.expect(_del_req, validate=True)
    @ns.marshal_with(_status_res)
    def post(self):
        """
        Move selected files to trash
        """
        args = request.args or request.json
        if not args:
            args = {}
        services.file.move2trash(**args)
        return {
            "status": True
        }


@ns.route('/restore', methods=['POST'])
class RestoreFiles(flask_restplus.Resource):
    @ns.expect(_del_req, validate=True)
    @ns.marshal_with(_status_res)
    def post(self):
        """
          Restore selected files from trash
        """
        args = request.args or request.json
        if not args:
            args = {}
        services.file.restore_files(**args)
        return {
            "status": True
        }


@ns.route('/perm_del', methods=['POST'])
class PermanentlyDelete(flask_restplus.Resource):
    @ns.expect(_del_req, validate=True)
    @ns.marshal_with(_status_res)
    def post(self):
        """
        Throw files away from system
        """
        args = request.args or request.json
        if not args:
            args = {}
        res = files.delete.delete(**args)
        return res


_file_share_req = ns.model('file_share_request', requests.share_req)
_star_req = ns.model('Add Star Request', requests.star_req)

@ns.route('/share', methods=['POST'])
class GetFiles(flask_restplus.Resource):
    @ns.expect(_file_share_req, validate=True)
    def post(self):
        args = request.args or request.json
        if not args:
            args = {}
        return services.file.share(args)

@ns.route('/add_star', methods=['POST'])
class AddStar(flask_restplus.Resource):
    @ns.expect(_star_req, validate=True)
    @ns.marshal_with(_status_res)
    def post(self):
        """
        Add star for a file
        """
        args = request.args or request.json
        file_id = args.get('file_id')
        services.file.add_star(file_id)
        return {
            "status": True
        }


@ns.route('/remove_star', methods=['POST'])
class RemoveStar(flask_restplus.Resource):
    @ns.expect(_star_req, validate=True)
    @ns.marshal_with(_status_res)
    def post(self):
        """
        Remove star for a file
        """
        args = request.args or requests.json
        file_id = args.get('file_id')
        services.file.remove_star(file_id)
        return {
            "status": True
        }


