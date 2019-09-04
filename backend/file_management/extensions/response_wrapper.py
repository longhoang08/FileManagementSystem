# coding=utf-8
import logging

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)


def wrap_response(data=None, message="", http_code=200, custom_code=''):
    """
    Return general HTTP response
    """
    res = {
        'code': http_code,
        'custom_code': custom_code,
        'success': http_code // 100 == 2,
        'message': message,
        'data': data
    }

    return res, http_code
