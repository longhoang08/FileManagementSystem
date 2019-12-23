# coding=utf-8
import logging

import flask_restplus
from flask import request

from file_management import services
from file_management.api.schema import requests
from file_management.extensions import Namespace

__author__ = 'jian'

from file_management.helpers.transformer import format_details_args

_logger = logging.getLogger(__name__)

ns = Namespace('files', description='File operations')

_file_details_req = ns.model('file_details_request', requests.file_details_req)


@ns.route('/details', methods=['POST'])
class GetFiles(flask_restplus.Resource):
    @ns.expect(_file_details_req, validate=True)
    def post(self):
        args = request.args or request.json
        format_details_args(args)
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
        res = services.file.drop_out(**args)
        return res


_file_share_req = ns.model('file_share_request', requests.share_req)
_star_req = ns.model('Add Star Request', requests.star_req)


@ns.route('/share', methods=['POST'])
class ShareFile(flask_restplus.Resource):
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
        args = request.args or request.json
        file_id = args.get('file_id')
        services.file.remove_star(file_id)
        return {
            "status": True
        }


_move_req = ns.model('Move Request', requests.move_req)


@ns.route('/move', methods=['POST'])
class MoveFile(flask_restplus.Resource):
    @ns.expect(_move_req, validate=True)
    @ns.marshal_with(_status_res)
    def post(self):
        """
        Move file to a another folder as long as user has privileges, else throw Exception!
        """
        services.file.move_files(**request.json)
        return {
            "status": True
        }

_copy_reg = ns.model('Copy Request', requests.copy_req)

@ns.route('/copy', methods=['POST'])
class CopyFile(flask_restplus.Resource):
    @ns.expect(_copy_reg, validate=True)
    @ns.marshal_with(_status_res)
    def post(self):
        """
        copy file to a another folder as long as user has privileges, else throw Exception!
        """
        services.file.copy_files(**request.json)
        return {
            "status": True
        }



_rename_req = ns.model('Rename Request', requests.rename_req)


@ns.route('/rename', methods=['POST'])
class RenameFile(flask_restplus.Resource):
    @ns.expect(_rename_req, validate=True)
    @ns.marshal_with(_status_res)
    def post(self):
        """
        Rename file
        """
        services.file.rename_file(**request.json)
        return {
            "status": True
        }

