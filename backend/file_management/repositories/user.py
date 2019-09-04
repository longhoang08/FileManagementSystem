# coding=utf-8
import logging

from sqlalchemy import or_

from file_management import models as m

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)


def save_user_to_database(**kwargs):
    user = m.User(**kwargs)
    m.db.session.add(user)

    return user


def find_one_by_email_or_username_ignore_case(email, username):
    user = m.User.query.filter(
        or_(
            m.User.username == username,
            m.User.email == email
        )
    ).first()  # type: m.User

    return user or None


def find_one_by_username(username):
    user = m.User.query.filter(
        m.User.username == username
    ).first()

    return user or None


def find_one_by_user_id(user_id):
    user = m.User.query.filter(
        m.User.id == user_id
    ).first()

    return user or None


def find_one_by_email(email):
    user = m.User.query.filter(
        m.User.email == email
    ).first()

    return user or None
