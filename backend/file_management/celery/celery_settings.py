import os
from celery.schedules import crontab

from file_management import app

CELERY_TASK_SERIALIZER = 'json'


BROKER_URL = f"redis://h:{os.environ['REDIS_PASSWORD']}@{os.environ['REDIS_HOST']}:{os.environ['REDIS_PORT']}"
# BROKER_URL = os.getenv('REDIS_URL', 'redis://h:123456789@redis-15913.c8.us-east-1-2.ec2.cloud.redislabs.com:15913') 
CELERY_ACCEPT_CONTENT = ['json']

CELERY_IMPORTS = ('file_management.celery.tasks')

CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'Asia/Ho_Chi_Minh'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
