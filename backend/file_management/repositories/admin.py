# coding=utf-8
import datetime
import logging

from sqlalchemy import or_

from file_management import models as m
from file_management.helpers import hash_password, get_environ

__author__ = 'Dat'
_logger = logging.getLogger(__name__)


def get_all_users(page, ipp):
    users = m.User.query.all().paginate(int(page), int(ipp), error_out=False).items
    return users


def search_users(username, page, ipp):
    users = m.User.query.filter(
        m.User.username.like(username + '%')
    ).paginate(int(page), int(ipp), error_out=False).items
    return users


def get_one_user(email):
    user = m.User.query.filter_by(email=email).first()
    return user
