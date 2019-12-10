# coding=utf-8
import logging

from file_management import models

__author__ = 'Dang'
_logger = logging.getLogger(__name__)


def find_file_by_file_id(file_id):
    file = models.File_info.query.filter(
            models.File_info.file_id == file_id
    ).first()
    return file or None
