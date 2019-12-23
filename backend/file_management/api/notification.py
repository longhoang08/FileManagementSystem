# coding=utf-8
import logging

import flask_restplus
from flask import request

from file_management import services
from file_management.extensions import Namespace
from file_management.services.notification import get_notification
from file_management.helpers.check_role import user_required
from file_management.api.schema import requests

_logger = logging.getLogger(__name__)

ns = Namespace('notifications', description='Notify to user')

_change_res = ns.model('notifications_req', requests.notification_viewed_req)


@ns.route('/viewed', methods=['POST'])
class UpdateNotificationViewd(flask_restplus.Resource):
    @user_required
    @ns.expect(_change_res, validate=True)
    def post(self):
        """ Mark as read """
        args = request.args or request.json
        return services.notification.marked_as_readed(args.get('ids'))
