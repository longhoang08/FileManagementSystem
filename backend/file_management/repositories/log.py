# coding=utf-8
import datetime
import logging
import random

_logger = logging.getLogger(__name__)

from file_management import models

def get_old_log():
    return = models.Log.query.filter(
        models.Log.created_at >= datetime.datetime.now()
    ).order_by(models.Log.created_at).all()

def del_old_log(logs)
    [models.db.session.delete(log) for log in logs]
    models.db.session.commit()