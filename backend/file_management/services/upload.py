# coding=utf-8
import logging
import os
import datetime
from file_management import repositories as repo
from file_management import helpers

__author__ = 'Dang'
_logger = logging.getLogger(__name__)


def create_file_info(path_upload, user_id, parent_id, file_name, file_size, file_id, mime_type, tags, **kwargs):
    modify_at = datetime.datetime.now()
    has_thumbnail =  helpers.is_has_thumbail(file_name)

    #TODO get thumnail url
    thumbnail_url =  helpers.get_thumbnail_url(file_id, file_name, path_upload)


    file_info = repo.upload.save_file_info_to_database(
        file_id = file_id,
        file_title = file_name,
        file_size = file_size,
        parent_id = parent_id,
        user_id = user_id,
        mime_type = mime_type,
        has_thumbnail = has_thumbnail,
        thumbnail_url = thumbnail_url,
        starred = False,
        trashed = False,
        version = 1,
        shared = False,
        tags = ','.join(tags),
        **kwargs
    ) 
    return file_info
