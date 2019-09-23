import logging

from file_management.repositories.log import del_old_log, get_old_log
_logger = logging.getLogger(__name__)

def save_log(date, message):
    pass

def del_log():
    logs = get_old_log()
    del_old_log(logs)