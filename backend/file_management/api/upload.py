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

        folders = utils.get_ancestors(parent_id)
        path_upload = '/'.join(folders)
        if not os.path.exists(path_upload):
            os.makedirs(path_upload)

        file_id = helpers.generate_file_id(user_id)
        file_name = fi.filename

        mime_type = ''

        try:
            mime_type = helpers.get_mime_type(file_name)
        except:
            pass

        try:
            # save files on server
            path_saved = os.path.join(path_upload, file_id)
            fi.save(path_saved)

            # get files size
            file_size = os.stat(path_saved).st_size
            tags = ['']

            # get tags if files is an image
            if ('image' in mime_type):
                tags = helpers.generate_image_tag(path_saved)
        except Exception as e:
            _logger.error(e)
            raise PathUploadNotFound()
        # get response
        upload_success = services.upload.create_file_info(path_upload, user_id, parent_id, file_name, file_size,
                                                          file_id, mime_type, tags)
        return upload_success
