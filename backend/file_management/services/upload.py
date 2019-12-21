# coding=utf-8
import logging
import os
import datetime
from file_management import repositories as repo
from file_management import helpers
from file_management.repositories.files import insert, utils
from file_management.extensions.custom_exception import PermissionException

__author__ = 'Dang'
_logger = logging.getLogger(__name__)


def create_file_info(path_upload, user_id, parent_id, file_name, file_size, file_id, mime_type, tags, **kwargs):
    modify_at = datetime.datetime.now()
    has_thumbnail = helpers.is_has_thumbail(file_name)

    thumbnail_url = helpers.get_thumbnail_url(file_id, file_name, path_upload)

    return insert.insert(file_id, file_name, file_size, parent_id,
                  user_id, mime_type, tags, thumbnail_url)


def write_file(fi, parent_id, user_id):

    folders = utils.get_ancestors(parent_id)
    path_upload = '/'.join(folders)
    if not os.path.exists(path_upload):
        os.makedirs(path_upload)

    file_id = helpers.generate_file_id(user_id)
    file_name = fi.filename

    mime_type = ''

    try:
        mime_type = helpers.get_mime_type(file_name)
    except:
        pass

    try:
        # save files on server
        path_saved = os.path.join(path_upload, file_id)
        fi.save(path_saved)

        # get files size
        file_size = os.stat(path_saved).st_size
        tags = ['']

        # get tags if files is an image
        if ('image' in mime_type):
            tags = helpers.generate_image_tag(path_saved)
    except Exception as e:
        _logger.error(e)
        raise PathUploadNotFound()
    # get response
    return create_file_info(path_upload, user_id, parent_id, file_name, file_size,
                            file_id, mime_type, tags)
