# coding=utf-8
import logging

from file_management import models
from file_management.helpers import hash_password

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)


def save_historic_password_to_database(**kwargs):
    historic_password = models.Password(**kwargs)
    models.db.session.add(historic_password)
    return historic_password


def find_all_password_by_userid(user_id):
    passwords = models.Password.query.filter(
        models.Password.user_id == user_id
    ).order_by(models.Password.created_at).all()
    return passwords


def delete_old_password(user_id):
    passwords = find_all_password_by_userid(user_id)
    if (len(passwords) > 5):
        models.db.session.delete(passwords[0])
        del passwords[0]
        models.db.session.commit()
    return passwords


def add_new_password_to_database(user_id, new_password):
    password_hash = hash_password(new_password)
    save_historic_password_to_database(user_id=user_id, password=password_hash)
    delete_old_password(user_id)


def add_new_hash_password_to_database(user_id, password_hash):
    save_historic_password_to_database(user_id=user_id, password=password_hash)
    delete_old_password(user_id)
