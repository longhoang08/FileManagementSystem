# coding=utf-8
import logging
import os
import flask_restplus
from flask import request, send_from_directory
from flask_restplus import reqparse
from file_management import services
from file_management import repositories
from werkzeug.datastructures import FileStorage
from file_management.extensions import Namespace
from file_management.extensions.custom_exception import CannotDownloadFile
from . import requests, responses
from file_management.services.file import utils
__author__ = 'Dang'
_logger = logging.getLogger(__name__)

ns = Namespace('download', description='Download file')

_download_req = ns.model('download_req', requests.download_file_req)

@ns.route('/', methods=['GET'])
class Download(flask_restplus.Resource):
    @ns.expect(_download_req, validate=True)
    def get(self):
        data = request.args or request.json
        file_id = data['file_id']
        
        try:
            UPLOAD_DIRECTORY = ""
            #file name located in server
            folders = utils.get_ancestors(file_id) 
            folders.append(file_id)
            path = '/'.join(folders)
            #real file name user see
            true_name = repositories.download.find_file_by_file_id(file_id).file_title
            return send_from_directory(UPLOAD_DIRECTORY, path, attachment_filename=true_name, as_attachment=True)
        except Exception as e:
            raise CannotDownloadFile()
       