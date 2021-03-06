# coding=utf-8
import logging
import os
import flask_restplus
from flask import send_from_directory, send_file
from file_management import repositories, services
from file_management.extensions import Namespace
from file_management.extensions.custom_exception import CannotDownloadFile
from . import requests
from ..repositories.files import utils
from file_management.constant import pathconst
from file_management.helpers.check_role import viewable_check

__author__ = 'Dang'
_logger = logging.getLogger(__name__)

ns = Namespace('download', description='Download files')

_download_req = ns.model('download_req', requests.download_file_req)


@ns.route('/<file_id>', methods=['GET'])
class Download(flask_restplus.Resource):
    def get(self, file_id):
        try:
            viewable_check(file_id)
            data = repositories.files.utils.get_file(file_id)
            true_name = data["file_title"]
            owner = data['owner']
            UPLOAD_DIRECTORY = pathconst.DOWNLOAD
            folders = utils.get_ancestors(owner)
            file_path = '/'.join(folders)
            file_path = os.path.join(file_path, file_id)
            return send_from_directory(UPLOAD_DIRECTORY, file_path, attachment_filename=true_name, as_attachment=True)
        except Exception as e:
            return str(e)
            raise CannotDownloadFile()


@ns.route('/thumbnail/<file_id>', methods=['GET'])
class Thumbnail(flask_restplus.Resource):
    """
        Get thumbnail file
    """

    def get(self, file_id):
        viewable_check(file_id)
        return send_file('../' + repositories.files.utils.get_file(file_id)["thumbnail_url"])
