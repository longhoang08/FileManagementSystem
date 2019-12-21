# coding=utf-8
import logging

from flask_jwt_extended import get_jwt_identity

from file_management.extensions.custom_exception import UserNotFoundException, DiffParentException
from file_management.helpers.check_role import user_required, owner_privilege_required
from file_management.repositories.files import FileElasticRepo
from file_management.repositories import files
from file_management import services

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


def extract_file_data_from_response(responses):
    if not responses:
        return {'result': {'files': []}}
    responses = responses.to_dict()
    hits = responses['hits']['hits']
    files = [item['_source'] for item in hits]
    return {'result': {'files': files}}


@owner_privilege_required
def move2trash(file_ids=None):
    """
    Move files to trash
    """
    if not isinstance(file_ids, list):
        return "Only accept `list` datatype"
    if len(file_ids) == 0:
        return "Nothing to move!"
    parent_of_first_file = files.utils.get_file(file_ids[0])['parent_id']
    for file_id in file_ids:
        parent_id = files.utils.get_file(file_id)['parent_id']
        if parent_id != parent_of_first_file:
            """
            All file must have same parent_id, else throws Exception
            """
            raise DiffParentException()
        move_one_file_to_trash(file_id)
    return True


@owner_privilege_required
def move_one_file_to_trash(file_id):
    files.update.update(file_id, trashed=True)


@user_required
def restore_files(file_ids=None):
    """
    Restore files from trash
    """
    if not file_ids:
        return "Nothing to restore!"
    for file_id in file_ids:
        files.update.update(file_id, trashed=False)
    return True


@user_required
def drop_out(file_ids):
    """
    Drop away files from ES
    """
    for file_id in file_ids:
        files.delete.delete(file_id)


@user_required
def add_star(file_id):
    files.update.update(file_id, star=True)


@user_required
def remove_star(file_id):
    files.update.update(file_id, star=False)
