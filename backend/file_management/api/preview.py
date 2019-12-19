# coding=utf-8
import logging

import flask_restplus
from flask import request
from file_management import services
from file_management.extensions import Namespace
from . import requests, responses
from file_management.services import preview
from file_management.services.file import utils
from file_management.constant import mime

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)

ns = Namespace('preview', description='Get docs, zip, image preview')

@ns.route('/<mime_type>/<file_id>', methods=['GET'])
class Get_preview(flask_restplus.Resource):
    def get(self, file_id, mime_type):
        "Get docs, zip, image preview. return path to file image or json or pdf"
        folders = utils.get_ancestors(file_id) 
        file_path = '/'.join(folders)
        
        if sum([x in mime_type for x in mime.image]):
            return preview.get_image_preview(file_id,file_path)
        elif sum([x in mime_type for x in mime.zip]):
            return preview.get_zip_preview(file_id,file_path)
        elif sum([x in mime_type for x in mime.docs]):
            return preview.get_docs_preview(file_id,file_path)
        



