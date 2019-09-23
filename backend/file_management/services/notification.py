import logging

from file_management import repositories
_logger = logging.getLogger(__name__)

def create_notification(user_id, message, **kwargs):
    noti = repositories.notification.get_all_notitfication(user_id=user_id, message=message, **kwargs)
    return noti

def get_notification(user_id, **kwargs):
    return repositories.notification.get_all_notitfication(user_id=user_id, **kwargs)