# coding=utf-8
import datetime
import logging

from flask import jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies

from file_management import models as m, services
from file_management import repositories
from file_management.constant import message
from file_management.extensions.custom_exception import MustConfirmEmailException, UserNotFoundException, \
    UserExistsException, NotInPendingException, NeedLoggedInException, PermissionException, BlockedException, \
    OwnerNotFoundException
from file_management.extensions.exceptions import BadRequestException
from file_management.helpers import validator, get_max_age, verify_password

__author__ = 'LongHB'

from file_management.repositories.user import find_one_by_user_id

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


# create new user, delete pending register request and save password to historic password
def confirm_user_by_email(email):
    new_user = create_user_from_pending_register(email)
    repositories.pending_register.delete_one_by_email(email)
    user_id = new_user.id
    hash_password = new_user.password
    repositories.password.add_new_hash_password_to_database(user_id, hash_password)
    return new_user


def fetch_user_status_by_email(email):
    from file_management.constant.user import Constant_user
    user = repositories.user.find_one_by_email(email)
    if (not user):
        return Constant_user.none_user
    return user


def handle_in_active(user):
    now = datetime.datetime.now().timestamp()
    if (now > user.un_block_at.timestamp()):
        repositories.user.un_block_user(user)
    else:
        raise BlockedException()


def check_username_and_password(username, password):
    if (validator.validate_username(username) and
            validator.validate_password(password)):
        pending_user = repositories.pending_register.find_one_by_username(username)
        if (pending_user):
            raise MustConfirmEmailException()
        user = repositories.user.find_one_by_username(username)
        if (not user):
            raise UserNotFoundException()
        if (not user.is_active):
            services.user.handle_in_active(user)
        if not verify_password(user.password, password):
            services.wrong_password.handle_wrong_password(user)
        return user
    else:
        raise BadRequestException(message.INVALID_USERNAME_OR_PASSWORD)


def login(username, password, **data):
    user = check_username_and_password(username, password)
    repositories.wrong_password.delete_all_wrong_password(user.id)
    # delete all wrong password history after login completed
    resp = jsonify(user.to_display_dict())
    access_token = create_access_token(identity=user.email)
    set_access_cookies(resp, access_token, max_age=get_max_age())
    return resp


def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp


def check_permission(user_email):
    from .token import check_jwt_token
    jwt_email = check_jwt_token()
    if (jwt_email == None):
        raise NeedLoggedInException()
    if (user_email != jwt_email):
        raise PermissionException()


def get_user_name_by_user_id(user_id):
    try:
        user_id = int(user_id)
        return find_one_by_user_id(user_id).fullname
    except Exception as e:
        _logger.error(e)
        raise OwnerNotFoundException()
