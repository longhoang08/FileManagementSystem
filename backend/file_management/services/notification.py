import logging

from file_management import repositories

_logger = logging.getLogger(__name__)


def create_notification(user_id, **kwargs):
    noti = repositories.notification.add_new_notification(user_id=user_id, **kwargs)
    return noti


def get_notification(user_id, **kwargs):
    notifications = repositories.notification.get_all_notitfication(user_id=user_id, **kwargs)
    notis = [noti.to_dict() for noti in notifications]
    return notis
