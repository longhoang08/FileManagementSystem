# coding=utf-8
import logging

from sqlalchemy import desc

_logger = logging.getLogger(__name__)

from file_management import models as m


def get_all_notitfication(user_id):
    return m.Notification.query.filter(
        m.Notification.user_id == user_id
    ).order_by(desc(m.Notification.created_at)).limit(10)


def get_notifications_by_ids(ids, user_id):
    return m.Notification.query.filter(
        m.Notification.id.in_(ids)
    ).filter(m.Notification.user_id == user_id).filter(m.Notification.viewed == False)


def marked_as_readed(notifications):
    updated = False
    for notification in notifications:
        notification.viewd = True
        updated = True
    m.db.session.commit()
    return {
        "updated": updated
    }


def add_new_notification(**kwargs):
    notification = m.Notification(**kwargs)
    m.db.session.add(notification)
    return notification
