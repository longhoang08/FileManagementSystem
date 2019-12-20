# coding=utf-8
import logging

from file_management import models

__author__ = 'Dang'
_logger = logging.getLogger(__name__)

def save_file_info_to_database(**kwargs):
    file_info = models.File_info(**kwargs)
    # models.db.session.add(file_info)
    return file_info

