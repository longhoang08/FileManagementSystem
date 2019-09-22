import os
import time
from celery import Celery
from file_management import app

celery = Celery('tasks', broker=app.config['REDIS_URL'], backend=app.config['REDIS_URL'])