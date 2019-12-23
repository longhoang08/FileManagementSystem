# coding=utf-8
import logging

import flask_restplus

from file_management.extensions import Namespace
from file_management.services.notification import get_notification
from file_management.helpers.check_role import user_required
from file_management.api.schema import requests

_logger = logging.getLogger(__name__)

ns = Namespace('notifications', description='Notify to user')

_change_res = ns.model('notifications_req', requests.notification_viewed_req)


@ns.route('/vỉewed', methods=['POST'])
class UpdateNotificationViewd(flask_restplus.Resource):
    @user_required
    @ns.expect(_change_res, validate=True)
    def post(self):
        """ Mark as read """
        pass