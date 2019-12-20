# coding=utf-8
import logging
import flask_restplus
from flask import send_from_directory
from file_management import repositories
from file_management.extensions import Namespace
from file_management.extensions.custom_exception import CannotDownloadFile
from . import requests
from ..repositories.files import utils
from file_management.constant import pathconst

__author__ = 'Dang'
_logger = logging.getLogger(__name__)

ns = Namespace('download', description='Download files')

_download_req = ns.model('download_req', requests.download_file_req)

@ns.route('/<user_id>/<file_id>', methods=['GET'])
class Download(flask_restplus.Resource):
    def get(self, user_id, file_id):
        try:
            UPLOAD_DIRECTORY = pathconst.DOWNLOAD
            folders = utils.get_ancestors(file_id) 
            file_path = '/'.join(folders)
            true_name = repositories.download.find_file_by_file_id(file_id).file_title
            return send_from_directory(UPLOAD_DIRECTORY, file_path, attachment_filename=true_name, as_attachment=True)
        except Exception as e:
            return str(e)
            raise CannotDownloadFile()
       