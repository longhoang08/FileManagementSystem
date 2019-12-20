 -1,13 +1,28 @@
# coding=utf-8
import logging

from flask_jwt_extended import get_jwt_identity

from file_management.extensions.custom_exception import UserNotFoundException
from file_management.helpers.check_role import user_required
from file_management.repositories.files import FileElasticRepo

__author__ = 'LongHB'

from file_management.repositories.user import find_one_by_email

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
def create_folder(args):
    parent_id = args.get('parent_id')
    file_title = args.get('file_title')
    file_id = helpers.generate_file_id(user_id)
    try:
        email = get_jwt_identity()
        user_id = find_one_by_email(email).id
        return insert.insert(file_id, file_title, 0, parent_id, user_id, "folder", "", "", starred=False)
    except Exception as e:
        _logger.error(e)
        raise UserNotFoundException()

   