# coding=utf-8
import logging

from file_management.repositories.file import FileElasticRepo

__author__ = 'jian'
_logger = logging.getLogger(__name__)

if __name__ == "__main__":
    es = FileElasticRepo()
    es.create_index_if_not_exist()
