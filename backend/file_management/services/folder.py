# coding=utf-8
import logging

from flask_jwt_extended import get_jwt_identity

from file_management import helpers
from file_management.extensions.custom_exception import UserNotFoundException, PermissionException
from file_management.helpers.check_role import user_required
from file_management.repositories.files import FileElasticRepo, insert

__author__ = 'LongHB'

from file_management.repositories.files.utils import get_role_of_user

from file_management.repositories.user import find_one_by_email
from file_management.services.file import extract_file_data_from_response, get_permision

_logger = logging.getLogger(__name__)


@user_required
def search(args):
    try:
        email = get_jwt_identity()
        args['user_id'] = find_one_by_email(email).id
    except Exception as e:
        _logger.error(e)
        raise UserNotFoundException()

    file_es = FileElasticRepo()
    response = file_es.search(args)
    return extract_file_data_from_response(response)


@user_required
def folder_details(args):
    try:
        email = get_jwt_identity()
        print(email)
        args['user_id'] = find_one_by_email(email).id
    except Exception as e:
        _logger.error(e)
        raise UserNotFoundException()

    folder_id = args.get('folder_id')
    permision = get_role_of_user(args.get('user_id'), folder_id)
    if not permision['viewable']:
        raise PermissionException("You are not allowed to view this folder.")
    es = FileElasticRepo()
    folder_details = es.get_children_of_folder(folder_id)
    children_id = folder_details['children_id']
    if not children_id:
        children_details = {'result': {'files': []}}
    else:
        children_details = search({
            'file_id': children_id, 'basic_info': True, 'user_id': '1', **args
        })
    del folder_details["children_id"]
    return {
        **folder_details,
        **permision,
        "children_details": children_details['result']['files']
    }


@user_required
def create_folder(args):
    parent_id = args.get('parent_id')
    file_title = args.get('file_title')
    try:
        email = get_jwt_identity()
        user_id = find_one_by_email(email).id
    except Exception as e:
        _logger.error(e)
        raise UserNotFoundException()
    file_id = helpers.generate_file_id(user_id)
    return insert.insert(file_id, file_title, 0, parent_id, user_id, "folder", "", "", starred=False)
