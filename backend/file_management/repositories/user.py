# coding=utf-8
import datetime
import logging

from sqlalchemy import or_

from file_management import models as m
from file_management.helpers import hash_password, get_environ

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)


def save_user_to_database(**kwargs):
    user = m.User(**kwargs)
    m.db.session.add(user)

    return user


def change_password(user, new_password):
    password_hash = hash_password(new_password)
    user.password = password_hash
    m.db.session.commit()
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


def block_user(user):
    user.is_active = False
    now = datetime.datetime.now()
    now_after_block_time = now + datetime.timedelta(minutes=int(get_environ('BLOCK_TIME')))
    user.un_block_at = now_after_block_time
    m.db.session.commit()
    return user


def un_block_user(user):
    user.is_active = True
    m.db.session.commit()
    return user


def get_users_by_ids(ids):
    return m.User.query.filter(
        m.User.id.in_(ids)
    ).filter(m.User.is_active == True).with_entities(m.User.email, m.User.fullname)
