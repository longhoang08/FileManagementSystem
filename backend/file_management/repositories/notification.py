# coding=utf-8
import logging

_logger = logging.getLogger(__name__)

from file_management import models as m

def get_all_notitfication(user_id):
    return m.Notification.query.filter(
        m.Notification.user_id == user_id
    ).order_by(m.Notification.created_at).all()

def add_new_notification(**kwargs):
    log = m.Log(**kwargs)
    m.db.session.add(log)
    return log