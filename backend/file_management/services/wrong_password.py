# coding=utf-8
import logging

from file_management import repositories
from file_management.constant import message
from file_management.extensions.custom_exception import BlockingException, WrongPasswordException

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)


def handle_wrong_password(user):
    id = user.get_id()
    num_of_wrong_passwords = repositories.wrong_password.number_of_wrong_password_by_user_id(id)
    repositories.wrong_password.save_wrong_password_to_redis(user_id=id)
    if (num_of_wrong_passwords >= 4):
        repositories.user.block_user(user)
        raise BlockingException(message.BLOCKING)
    raise WrongPasswordException(message.WRONG_PASSWORD)
