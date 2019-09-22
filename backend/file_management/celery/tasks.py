import os
import time
from celery import Celery
from file_management import app

celery = Celery('tasks', broker=app.config['REDIS_URL'], backend=app.config['REDIS_URL'])


@celery.task(name='tasks.add')
def del_old_log(x: int, y: int) -> int:
    return x + y

def send_mail(email: str):
    print(f"Sending mail to {email}")