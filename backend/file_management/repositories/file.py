# coding=utf-8
import logging

from elasticsearch_dsl import query, Search

from config import FILES_INDEX
from file_management.models.file import index_config
from file_management.repositories.es_base import EsRepositoryInterface

__author__ = 'jian'
_logger = logging.getLogger(__name__)


class FileElasticRepo(EsRepositoryInterface):
    def __init__(self):
        super().__init__()
        self._index = FILES_INDEX
        self.mappings = index_config['mappings']
        self.settings = index_config['settings']
        self.id_key = 'file_id'

    def search(self, args):
        """
        exec query and return response
        :param args:
        :return:
        """
        file_es = self.build_query(args)
        # print(json.dumps(file_es.to_dict()))
        responses = file_es.using(self.es).index(self._index).execute()
        return responses

    def build_query(self, args):
        """
        Build query for es
        :param args:
        :return:
        """
        conditions = query.Bool(
            must=query.MatchAll()
        )
        file_es = self.build_file_es(args, conditions)
        return file_es

    def build_file_es(self, args, search_condition):
        file_es = Search() \
            .query(search_condition)
        file_es = file_es.sort(*self.sort_condition(args))
        file_es = self.add_page_limit_to_file_es(args, file_es)
        return file_es

    def add_page_limit_to_file_es(self, args, file_es):
        _limit = args.get('_limit') if args.get('_limit') else 20
        file_es = file_es[0:_limit]
        return file_es

    def sort_condition(self, args):
        return [self.sort_by_score()]

    def sort_by_score(self):
        return {
            '_score': {
                'order': 'desc'
            }
        }
