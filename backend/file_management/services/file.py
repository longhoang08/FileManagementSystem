# coding=utf-8
import logging

from flask_jwt_extended import get_jwt_identity

from file_management.extensions.custom_exception import UserNotFoundException
from file_management.helpers.check_role import user_required
from file_management.repositories.files import FileElasticRepo
from file_management.repositories.files import update
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


def get_permision(user_id, file_ids):
    file_es = FileElasticRepo()
    response = file_es.get_permission(user_id, file_ids)
    response = extract_file_data_from_response(response)
    files = response['result']['files']
    result = {
        'editable': False,
        'view': False
    }
    if not files:
        return result
    file = files[0]
    if file['owner'] == user_id or (file['share_mode'] == 1 and file['editable'] == True):
        result['editable'] = True
    result['view'] = True
    return {
        'editable': file['editable'],
        'view': True
    }


def extract_file_data_from_response(responses):
    if not responses:
        return {'result': {'files': []}}
    responses = responses.to_dict()
    hits = responses['hits']['hits']
    files = [item['_source'] for item in hits]
    return {'result': {'files': files}}


@user_required
def share(args):
    try:
        email = get_jwt_identity()
        args['user_id'] = find_one_by_email(email).id
    except Exception as e:
        _logger.error(e)
        raise UserNotFoundException()
    user_shared = [find_one_by_email(email).id for email in args['emails']]
    file_id = args['file_id']
    if args['private']:
        share_mode = 0
        return update.update_share(file_id, share_mode)
    elif args['share_by_link']:
        share_mode = 1
        return update.update_share(file_id, share_mode, user_shared)
    else:
        share_mode = 2
        return update.update_share(file_id, share_mode)
    
