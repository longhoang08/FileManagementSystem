# coding=utf-8
import datetime
import logging
import random

from file_management.helpers import get_time_range_to_block
from file_management.models import redis_client

__author__ = 'longhb'
_logger = logging.getLogger(__name__)


def save_wrong_password_to_redis(user_id):
    key = str(user_id) + '-' + str(random.randint(1000, 9999))
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    redis_client.set(key, now, ex=get_time_range_to_block())


def number_of_wrong_password_by_user_id(user_id):
    return len(redis_client.keys(pattern=str(user_id) + '*'))


def delete_all_wrong_password(user_id):
    wrong_password_keys = redis_client.keys(pattern=str(user_id) + '*')
    for key in wrong_password_keys:
        redis_client.delete(key)
