# coding=utf-8
import logging

from file_management import models as m
from file_management import repositories
from file_management.constant import message
from file_management.extensions.custom_exception import MustConfirmEmailException, UserNotFoundException, \
    UserExistsException, NotInPendingException
from file_management.extensions.exceptions import BadRequestException
from file_management.helpers import validator

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)


# create user from a register after validate
def create_user(username, email, fullname, password, **kwargs):
    """
    Validate post data and create a new user
    :param str username:
    :param str email:
    :param str password:
    :param str fullname:
    :param kwargs:
    :return: a new user
    :rtype: m.User
    """
    existed_user = repositories.user.find_one_by_email_or_username_ignore_case(
        email, username)
    if existed_user:
        message = "User with username {username} "
        "or email {email} already existed!".format(
            username=username,
            email=email
        )
        raise UserExistsException(message)

    user = repositories.user.save_user_to_database(
        username=username,
        email=email,
        fullname=fullname,
        password=password,
        **kwargs
    )
    return user


def create_user_from_pending_register(email):
    pending_register = repositories.pending_register.find_one_by_email(email)
    if (not pending_register):
        raise NotInPendingException()
    pending_register_dict = pending_register.to_dict()
    username = pending_register_dict.get('username')
    fullname = pending_register_dict.get('fullname')
    password = pending_register_dict.get('password')
    return create_user(username, email, fullname, password)


def check_username_and_password(username, password, **kwargs):
    if (validator.validate_username(username) and
            validator.validate_password(password)):
        pending_user = repositories.pending_register.find_one_by_username(username)
        if (pending_user):
            raise MustConfirmEmailException()

        user = repositories.user.find_one_by_username(username)

        if (not user):
            raise UserNotFoundException()

        return user
    else:
        raise BadRequestException(message.INVALID_USERNAME_OR_PASSWORD)
