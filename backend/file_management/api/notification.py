# coding=utf-8
import logging

import flask_restplus
from flask import request

from file_management import services
from file_management.extensions import Namespace
from file_management.services.notification import get_notification
from .schema.response import ResSchema
from .schema.request import ReqSchema

_logger = logging.getLogger(__name__)

ns = Namespace('notifications', description='Notify to user')

_change_res = ns.model('notifications_res', ResSchema.make_notification_res(ns))

@ns.route('/<user_id>', methods=['GET'])
class Get_notification(flask_restplus.Resource):
    """ Notify to user """
    @ns.marshal_with(_change_res)
    def get(self):    
        return get_notification(user_id)
