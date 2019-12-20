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


def extract_file_data_from_response(responses):
    if not responses:
        return {'result': {'files': []}}
    responses = responses.to_dict()
    hits = responses['hits']['hits']
    files = [item['_source'] for item in hits]
    return {'result': {'files': files}}
