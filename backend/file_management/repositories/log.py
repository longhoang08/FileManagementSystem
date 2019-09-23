# coding=utf-8
import datetime
import logging
import random

_logger = logging.getLogger(__name__)

from file_management import models as m

def get_old_log():
    return m.Log.query.filter(
        m.Log.created_at >= datetime.datetime.now()
    ).order_by(m.Log.created_at).all()

def get_all_log(folder_id):
    return  m.Log.query.filter(
        m.Log.folder_id == folder_id
    ).order_by(m.Log.created_at).all()

def del_old_log(logs):
    [m.db.session.delete(log) for log in logs]
    m.db.session.commit()

def save_log_to_db(**kwargs):
    log = m.Log(**kwargs)
    m.db.session.add(log)
    return log