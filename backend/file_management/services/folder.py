# coding=utf-8
import logging

from flask_jwt_extended import get_jwt_identity

from file_management import helpers
from file_management.extensions.custom_exception import UserNotFoundException, PermissionException, \
    ParentFolderNotExistException
from file_management.helpers.check_role import user_required, get_email_in_jwt, viewable_check
from file_management.helpers.transformer import add_user_name_to_files, extract_file_data_from_response
from file_management.repositories.files import FileElasticRepo, insert

__author__ = 'LongHB'

from file_management.repositories.files.utils import get_role_of_user, is_this_file_exists, get_parse_url

from file_management.repositories.user import find_one_by_email
from file_management.services.user import get_user_name_by_user_id

_logger = logging.getLogger(__name__)


def folder_details(args):
    folder_id = args.get('folder_id')
    permission, user_info = viewable_check(folder_id, error_message="You are not allowed to view this folder")
    user_id = user_info.get('user_id')
    es = FileElasticRepo()
    folder_details = es.get_children_of_folder(folder_id)
    children_id = folder_details['children_id']
    children_details = {'result': {'files': []}} if not children_id else get_files_in_folders(children_id, args)

    del folder_details["children_id"]

    folder_owner_id = folder_details.get('owner')
    folder_details['owner'] = {
        'id': folder_owner_id,
        'name': get_user_name_by_user_id(folder_owner_id)
    }

    children_details = children_details['result']['files']
    add_user_name_to_files(children_details)
    return {
        **folder_details,
        **permission,
        'parse_urls': get_parse_url(folder_id, user_id),
        "children_details": children_details
    }


def get_files_in_folders(childrent_id, args):
    args['file_id'] = childrent_id
    args['is_folder_api'] = True
    args['basic_info'] = True
    file_es = FileElasticRepo()
    response = file_es.search(args)
    return extract_file_data_from_response(response)


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
    if not is_this_file_exists(parent_id):
        raise ParentFolderNotExistException()

    file_id = helpers.generate_file_id(user_id)

    return insert.insert(file_id, file_title, 0, parent_id, user_id, "folder", "", "", starred=False)
