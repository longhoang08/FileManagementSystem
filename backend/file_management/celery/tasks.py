from celery import Celery

from file_management import app
from file_management.services.mail_service import send_email

celery = Celery('tasks', broker=app.config['REDIS_URL'], backend=app.config['REDIS_URL'])


@celery.task(name='tasks.add')
def del_old_log(x: int, y: int) -> int:
    return x + y

@celery.task(name='tasks.send_email', bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 10, 'countdown': 10 * 60})
def send_mail(subject: str, contact: str, body_message:str):
    """ 
    countdown: int (second) 
    auto retry if exception
    The bind argument means that the function will be a “bound method” so that you can access attributes and methods on the task type instance.
    """
    send_email(subject, contact, body_message)