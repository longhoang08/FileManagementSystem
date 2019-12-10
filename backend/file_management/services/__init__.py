# coding=utf-8
import logging

from flask_mail import Mail

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)

from . import user
from . import pending_register
from . import mail_service
from . import token
from . import password
from . import wrong_password
from . import log
from . import notification
from . import file

my_mail = Mail()


def init_app(app):
    my_mail.init_app(app)
