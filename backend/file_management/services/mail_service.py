# coding=utf-8
import logging

from flask_mail import Message

from file_management.extensions.custom_exception import CantSendEmailException

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)


def send_email(subject, contact, body_message):
    from file_management.services import my_mail
    msg = Message(subject,
                  sender='viem.t.viemde@gmail.com',
                  recipients=[contact],
                  html=body_message)
    try:
        my_mail.send(msg)
    except Exception as e:
        _logger.error(e)
        raise CantSendEmailException()
