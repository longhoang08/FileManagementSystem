# coding=utf-8
import logging

import flask_restplus
from flask import send_file
from file_management.extensions import Namespace
from file_management.services import preview
from ..repositories.files import utils
from file_management.constant import mime

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)

ns = Namespace('preview', description='Get docs, zip, image preview')


@ns.route('/<mime_type>/<file_id>', methods=['GET'])
class Get_preview(flask_restplus.Resource):
    def get(self, file_id, mime_type):
        "Get docs, zip, image preview. return path to files image or json or pdf"
        folders = utils.get_ancestors(file_id) 
        file_path = '/'.join(folders)

        if sum([x in mime_type for x in mime.image]):
            return send_file("../" + preview.get_image_preview(file_id, file_path))
        elif sum([x in mime_type for x in mime.zip]):
            return send_file("../" + preview.get_zip_preview(file_id, file_path))
        elif sum([x in mime_type for x in mime.docs]):
            return send_file("../" + preview.get_docs_preview(file_id, file_path))
        elif sum([x in mime_type for x in mime.video]):
            return send_file("../" + file_path,mimetype='video/mp4')
        elif sum([x in mime_type for x in mime.audio]):
            return send_file("../" + file_path,mimetype='audio/mpeg')
        else:
            return "Can not preview"
