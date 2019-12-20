# coding=utf-8
import logging

__author__ = 'LongHB'

from flask_jwt_extended import get_jwt_identity

from file_management.repositories.file import FileElasticRepo
from .file import search
from ..extensions.custom_exception import UserNotFoundException
from ..helpers.check_role import user_required
from ..repositories.pending_register import find_one_by_email

_logger = logging.getLogger(__name__)


@user_required


def folder_details(args):
    try:
        email = get_jwt_identity()
        args['user_id'] = find_one_by_email(email).id
    except Exception as e:
        _logger.error(e)
        raise UserNotFoundException()

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
