# coding=utf-8
import logging

__author__ = 'longhb'

from config import FILES_INDEX
from file_management.repositories.file import FileElasticRepo,
from .file import search
from file_management.repositories.files import insert

_logger = logging.getLogger(__name__)


def create_folder(args):
    # check token
    parent_id = args.get('parent_id')
    folder_name = args.get('folder_name')

    insert(file_id, folder, file_size, parent_id, user_id, "folder", "","", starred=False)


def folder_details(args):
    # check token
    from file_management.repositories.files import es
    folder_id = args.get('folder_id')
    es = FileElasticRepo()
    folder_details = es.get_children_of_folder(folder_id)
    children_id = folder_details['children_id']

    if not children_id:
        children_details = {'result': {'files': []}}
    else:
        children_details = search({
            'file_id': children_id, 'basic_info': True, 'user_id': '1', **args
        })
    return {
        **folder_details,
        "children_details": children_details['result']['files']
    }