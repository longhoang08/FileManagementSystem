# coding=utf-8
import logging
import os
import datetime
from file_management import repositories as repo
from file_management.helpers import generate_file_id

__author__ = 'Dang'
_logger = logging.getLogger(__name__)


def create_file_info(user_id, parent_id, file_name, file_size, **kwargs):
    file_id = generate_file_id(user_id)
    create_at = datetime.datetime.now()
    modify_at = datetime.datetime.now()
    file_info = repo.upload.save_file_info_to_database(
        file_id = file_id,
        file_title = file_name,
        file_size = file_size,
        created_at = create_at,
        parent_id = parent_id,
        user_id = user_id, 
        **kwargs
    ) 
    return file_info
