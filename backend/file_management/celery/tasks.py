from celery import Celery

# from file_management import app


# celery = Celery('tasks', broker=app.config['REDIS_URL'], backend=app.config['REDIS_URL'])

app = Celery()
app.config_from_object("file_management.celery.celery_settings")

@app.task(name='tasks.add')
def del_old_log(x: int, y: int) -> int:
    print("dhdhdhdhdhdhd")
    return x + y

@app.task(name='tasks.send_email', autoretry_for=(Exception,), retry_kwargs={'max_retries': 10, 'countdown': 10 * 60})
def send_mail(subject: str, contact: str, body_message:str):
    """ 
    countdown: int (second) 
    auto retry if exception
    The bind argument means that the function will be a “bound method” so that you can access attributes and methods on the task type instance.
    """
    from file_management.services.mail_service import send_email
    send_email(subject, contact, body_message)