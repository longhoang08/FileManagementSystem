# coding=utf-8
import logging
import os
import flask_restplus
from flask import request, send_from_directory
from flask_restplus import reqparse
from file_management import services
from werkzeug.datastructures import FileStorage
from file_management.extensions import Namespace
from file_management.extensions.custom_exception import CannotDownloadFile
from . import requests, responses

__author__ = 'Dang'
_logger = logging.getLogger(__name__)

ns = Namespace('download', description='Download file')

_download_req = ns.model('download_req', requests.download_file_req)

@ns.route('/', methods=['GET'])
class Download(flask_restplus.Resource):
    # @ns.expect(_download_req, validate=True)
    def get(self):
        #TODO path = elasticsearch.get(FileID)
        try:
            UPLOAD_DIRECTORY = ""
            #file name located in server
            path = ""
            #real file name user see
            true_name = ""
            return send_from_directory(UPLOAD_DIRECTORY, path, attachment_filename=true_name, as_attachment=True)
        except Exception as e:
            raise CannotDownloadFile()
       