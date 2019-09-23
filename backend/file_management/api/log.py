# coding=utf-8
import logging

import flask_restplus
from flask import request

from file_management import services
from file_management.extensions import Namespace
from file_management.services.log import get_all_log
from .schema.response import ResSchema
from .schema.request import ReqSchema

_logger = logging.getLogger(__name__)

ns = Namespace('logs', description='Log about create edit remove file in folder')

_change_res = ns.model('logs_res', ResSchema.make_logs_res(ns))

@ns.route('/<folder_id>', methods=['GET'])
class Get_log(flask_restplus.Resource):
    """ Log about create edit remove file in folder """
    @ns.marshal_with(_change_res)
    def get(self):    
        return get_all_log(folder_id)
