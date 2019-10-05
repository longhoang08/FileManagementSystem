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
from . import requests, responses

__author__ = 'Dang'
_logger = logging.getLogger(__name__)

ns = Namespace('download', description='Download file')

_upload_res = ns.model('upload_res', responses.file_uploaded_res)
_download_req = ns.model(download_red, requests.download_file_req)

@ns.route('/', methods=['GET'])
class Download(flask_restplus.Resource):
    @ns.expect(_download_req, validate=True)
    def get(self):
        
        


