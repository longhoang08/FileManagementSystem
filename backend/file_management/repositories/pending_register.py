# coding=utf-8
import logging

from sqlalchemy import or_

from file_management import models

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)


def save_pending_register_to_database(**kwargs):
    pending_register = models.Pending_register(**kwargs)
    models.db.session.add(pending_register)

    return pending_register


def find_one_by_email_or_username(email, username):
    pending_register = models.Pending_register.query.filter(
        or_(
            models.Pending_register.username == username,
            models.Pending_register.email == email
        )
    ).first()

    return pending_register or None


def find_one_by_email(email):
    pending_register = models.Pending_register.query.filter(
        models.Pending_register.email == email
    ).first()

    return pending_register or None


def find_one_by_username(username):
    pending_register = models.Pending_register.query.filter(
        models.Pending_register.username == username
    ).first()

    return pending_register or None


def delete_one_by_email(email):
    models.Pending_register.query.filter(
        models.Pending_register.email == email
    ).delete()
    models.db.session.commit()
