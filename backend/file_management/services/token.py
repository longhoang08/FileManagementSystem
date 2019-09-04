# coding=utf-8
import logging
import os

from flask_jwt_extended import get_jwt_identity, jwt_required

from file_management.extensions.custom_exception import InvalidTokenException
from file_management.helpers import encode_token

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)


def gen_jwt_token_when_login(email, **kwargs):
    jwt_token = encode_token(email, int(os.environ['TOKEN_UPTIME']))
    return jwt_token


@jwt_required
def verifile_token():
    email = get_jwt_identity()
    return email


def check_jwt_token():
    try:
        email = verifile_token()
        return email
    except:
        raise InvalidTokenException("Invalid token or Signal expired")
