# coding=utf-8
import logging
import os

from file_management import helpers
from file_management.repositories.files import insert, utils
from file_management.extensions.custom_exception import PathUploadNotFound
from file_management.repositories.file import FileElasticRepo

__author__ = 'Dang'
_logger = logging.getLogger(__name__)


def create_file_info(path_upload, user_id, parent_id, file_name, file_size, file_id, mime_type, tags, **kwargs):
    thumbnail_url = helpers.get_thumbnail_url(file_id, file_name, path_upload)

    insert.insert(file_id, file_name, file_size, parent_id,
                  user_id, mime_type, tags, thumbnail_url)

    return {
        'file_id': file_id,
        'file_name': file_name,
        'tags': tags,
        'file_size': file_size
    }


def check_duplicate(file_name, parent_id):
    es = FileElasticRepo()
    list_child = es.get_children_of_folder(parent_id)['children_id']
    list_name = [utils.get_file(fileid)["file_title"] for fileid in list_child]
    if file_name in list_name:
        return check_duplicate("copy of " + file_name, parent_id)
    else:
        return str(file_name)


def write_file(fi, parent_id, user_id):
    folders = utils.get_ancestors(str(user_id))
    path_upload = '/'.join(folders)
    if not os.path.exists(path_upload):
        os.makedirs(path_upload)

    file_id = helpers.generate_file_id(user_id)
    file_name = check_duplicate(fi.filename, parent_id)

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

        # # get tags if files is an image
        # if ('image' in mime_type):
        #     tags = helpers.generate_image_tag(path_saved)
    except Exception as e:
        _logger.error(e)
        raise PathUploadNotFound()
    # get response
    return create_file_info(path_upload, user_id, parent_id, file_name, file_size,
                            file_id, mime_type, tags)
