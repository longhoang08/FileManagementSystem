# coding=utf-8
import datetime
import logging

from file_management import models as m, services
from file_management import repositories
from file_management.extensions.custom_exception import UserNotFoundException, BlockedException

__author__ = 'Dat'
_logger = logging.getLogger(__name__)


def get_all_users(page=1, ipp=10):
    users = repositories.admin.get_all_users(page, ipp)
    users_dict = [user.to_dict() for user in users]
    return users_dict


def search_users(username, page=1, ipp=10):
    users = repositories.admin.search_users(username, page, ipp)
    users_dict = [user.to_dict() for user in users]
    return users_dict


def block_user(email):
    user = repositories.admin.get_one_user(email)
    if user is None:
        raise UserNotFoundException()
    blocked_user = repositories.user.block_user(user)
    return blocked_user.to_dict()


def un_block_user(email):
    user = repositories.admin.get_one_user(email)
    if user is None:
        raise UserNotFoundException()
    un_blocked_user = repositories.user.un_block_user(user)
    return un_blocked_user.to_dict()
