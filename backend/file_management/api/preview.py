# coding=utf-8
import logging

import flask_restplus
from flask import send_file

from file_management import repositories
from file_management.constant import mime
from file_management.extensions import Namespace
from file_management.helpers.check_role import viewable_check
from file_management.services import preview
from ..repositories.files import utils

__author__ = 'LongHB'

_logger = logging.getLogger(__name__)

ns = Namespace('preview', description='Get docs, zip, image preview')


@ns.route('/<file_id>', methods=['GET'])
class Get_preview(flask_restplus.Resource):
    def get(self, file_id):
        "Get docs, zip, image preview. return path to files image or json or pdf"
        viewable_check(file_id)
        data = repositories.files.utils.get_file(file_id)
        mime_type = data["file_type"]
        folders = utils.get_ancestors(data['owner'])
        file_path = '/'.join(folders) + '/' + file_id
        print(file_path)
        if sum([x in mime_type for x in mime.image]):
            return send_file("../" + file_path, mimetype=mime_type)
        elif sum([x in mime_type for x in mime.zip]):
            return send_file("../" + preview.get_zip_preview(file_id, file_path))
        elif sum([x in mime_type for x in mime.docs]):
            return send_file("../" + preview.get_docs_preview(file_id, file_path))
        elif sum([x in mime_type for x in mime.video]):
            return send_file("../" + file_path, mimetype='video/mp4')
        elif sum([x in mime_type for x in mime.audio]):
            return send_file("../" + file_path, mimetype=mime_type)
        else:
            return "Can not preview"
