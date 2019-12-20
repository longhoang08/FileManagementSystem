# coding=utf-8
import logging
import os
import flask_restplus
from flask import request

from flask_restplus import reqparse
from file_management import services
from werkzeug.datastructures import FileStorage
from file_management.extensions import Namespace
from file_management.extensions.custom_exception import PathUploadNotFound
from . import responses
from file_management import helpers
from ..repositories.files import utils

__author__ = 'Dang'
_logger = logging.getLogger(__name__)

ns = Namespace('upload', description='Upload files')

_upload_res = ns.model('upload_res', responses.file_uploaded_res)


@ns.route('/', methods=['POST'])
# @ns.route('/<user_id>/<parent_id>', methods=['POST'])
class Upload(flask_restplus.Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('in_file', type=FileStorage, location='files')
    parser.add_argument('user_id', type=int, help='user_id')
    parser.add_argument('parent_id', type=str, help='parent_id')

    @ns.marshal_with(_upload_res)
    @ns.expect(parser, validate=True)
    def post(self):
        user_id = request.form['user_id']
        parent_id = request.form['parent_id']
        folders = utils.get_ancestors(parent_id)
        path_upload = '/'.join(folders)

        if not os.path.exists(path_upload):
            os.makedirs(path_upload)


        fi = request.files.get('in_file')
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
            if('image' in mime_type):
                tags = helpers.generate_image_tag(path_saved)
        except Exception as e:
            _logger.error(e)
            raise PathUploadNotFound()
        # get response
        upload_success = services.upload.create_file_info(path_upload, user_id, parent_id, file_name, file_size, file_id, mime_type, tags)
        return upload_success