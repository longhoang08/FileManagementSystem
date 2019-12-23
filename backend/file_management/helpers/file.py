# coding=utf-8
import logging

__author__ = 'LongHB'

from file_management.helpers.transformer import extract_file_data_from_response
from file_management.repositories.file import FileElasticRepo

_logger = logging.getLogger(__name__)


def check_duplicate_when_upload_or_create(folder_id, name):
    es = FileElasticRepo()
    response = es.query_to_check_duplicate_when_upload_or_create(folder_id, name)
    response = extract_file_data_from_response(response)
    return not not response['result']['files']
