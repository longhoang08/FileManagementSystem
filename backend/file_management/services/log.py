import logging

from file_management import repositories
_logger = logging.getLogger(__name__)

def save_log(folder_id, message, **kwargs):
    log = repositories.log.save_log(folder_id=folder_id, message=message, **kwargs)
    return log

def del_log():
    logs = repositories.log.get_old_log()
    repositories.log.del_old_log(logs)

def get_all_log(folder_id):
    return repositories.log.get_all_log(folder_id)