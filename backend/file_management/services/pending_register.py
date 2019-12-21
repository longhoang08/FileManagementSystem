# coding=utf-8
import logging
import os

from file_management import repositories as repo
from file_management.extensions.custom_exception import RegisterBeforeException, UserExistsException
from file_management.extensions.exceptions import BadRequestException
from file_management.helpers import encode_token
from file_management.helpers import validate_register, hash_password
from file_management.templates import email_template
# from file_management.services import mail_service

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)


def create_pending_register(username, email, fullname, password, **kwargs):
    if validate_register(username, email, fullname, password):
        existed_user = repo.user.find_one_by_email_or_username_ignore_case(
            email, username)
        # check if user existed
        if existed_user:
            message = ("User with username {username} " +
                       "or email {email} already existed!").format(
                username=username,
                email=email
            )
            raise UserExistsException(message)
        # check if that user registed before
        existed_pending_register = repo.pending_register.find_one_by_email_or_username(email, username)
        if (existed_pending_register):
            message = ("User with username {username} " +
                       "or email {email} already register before").format(
                username=username,
                email=email
            )
            raise RegisterBeforeException(message)

        # save pending register to database
        pending_register = repo.pending_register.save_pending_register_to_database(
            username=username,
            email=email,
            fullname=fullname,
            password=hash_password(password)
        )
        return pending_register

    else:
        raise BadRequestException("Invalid user data specified!")


def send_confirm_email(username, email, fullname, **kwargs):
    confirm_token = encode_token(email, int(os.environ['TOKEN_UPTIME']))
    active_link = os.environ['SERVER_BASE_URL'] + 'register/confirm_email/' + confirm_token
    msg_html = email_template.gen_confirm_email_body_template(fullname, username, active_link)
    from file_management.celery.tasks import send_mail
    send_mail("uFile's email confirmation", email, msg_html)
