import logging

from file_management import repositories
from file_management.repositories.notification import get_notifications_by_ids
from file_management.repositories.user import find_one_by_username, find_one_by_email

_logger = logging.getLogger(__name__)


def create_notification(user_id, **kwargs):
    noti = repositories.notification.add_new_notification(user_id=user_id, **kwargs)
    return noti


def get_notification(user_id, **kwargs):
    notifications = repositories.notification.get_all_notitfication(user_id=user_id, **kwargs)
    notis = [noti.to_dict() for noti in notifications]
    return notis


def marked_as_readed(ids):
    from file_management.helpers.check_role import get_email_in_jwt
    email = get_email_in_jwt()
    user = find_one_by_email(email)
    user_id = user.id
    notifications = get_notifications_by_ids(ids, user_id)
    return repositories.notification.marked_as_readed(notifications)
