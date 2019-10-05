# coding=utf-8
import logging

import flask_restplus

from file_management.extensions import Namespace
from file_management.services.notification import get_notification
from . import responses

_logger = logging.getLogger(__name__)

ns = Namespace('notifications', description='Notify to user')

_change_res = ns.model('notifications_res', responses.notification_field)

@ns.route('/<user_id>', methods=['GET'])
class Get_notification(flask_restplus.Resource):
    @ns.marshal_list_with(_change_res)
    def get(self):
        """ Notify to user """
        return get_notification(user_id)
