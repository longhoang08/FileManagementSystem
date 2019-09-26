# coding=utf-8
import logging

import flask_restplus

from file_management.extensions import Namespace
from file_management.services.log import get_all_log
from . import responses

_logger = logging.getLogger(__name__)

ns = Namespace('logs', description='Log about create edit remove file in folder')

_change_res = ns.model('logs_res', responses.log_field)

@ns.route('/<folder_id>', methods=['GET'])
class Get_log(flask_restplus.Resource):
    @ns.marshal_list_with(_change_res)
    def get(self):
        """ Log about create edit remove file in folder """
        return get_all_log(folder_id)
