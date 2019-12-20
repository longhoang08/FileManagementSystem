# coding=utf-8
import logging

from file_management.repositories.files import FileElasticRepo

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)


def search(args):
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
