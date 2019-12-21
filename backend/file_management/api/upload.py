# coding=utf-8
import logging
import os
import flask_restplus
from flask import request
from flask_jwt_extended import get_jwt_identity

from flask_restplus import reqparse
from file_management import services
from werkzeug.datastructures import FileStorage
from file_management.extensions import Namespace
from file_management.extensions.custom_exception import PathUploadNotFound, UserNotFoundException
from . import responses
from file_management import helpers
from ..helpers.check_role import user_required
from ..repositories.files import utils

__author__ = 'Dang'

from ..repositories.user import find_one_by_email

_logger = logging.getLogger(__name__)

ns = Namespace('upload', description='Upload files')

_upload_res = ns.model('upload_res', responses.file_uploaded_res)


@ns.route('/', methods=['PUT'])
class Upload(flask_restplus.Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('in_file', type=FileStorage, location='files')
    parser.add_argument('parent_id', type=str, help='parent_id')

    @ns.marshal_with(_upload_res)
    @ns.expect(parser, validate=True)
    @user_required
    def put(self):
        try:
            email = get_jwt_identity()
            user_id = find_one_by_email(email).id
        except Exception as e:
            _logger.error(e)
            raise UserNotFoundException()

        parent_id = request.form['parent_id']
        fi = request.files.get('in_file')

        return services.upload.write_file(fi, parent_id, user_id)
        
