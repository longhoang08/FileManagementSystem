# coding=utf-8
import logging

import elasticsearch.helpers
from elasticsearch import Elasticsearch

from config import ELASTIC_HOST

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)


def get_update_body_query(data):
    return {
        "doc": data,
        "doc_as_upsert": True
    }


class EsRepositoryInterface:
    def __init__(self):
        self.es = Elasticsearch(ELASTIC_HOST)
        self._index = None
        self.id_key = ''
        self.settings = {}
        self.mappings = {}

    def create_index_if_not_exist(self):
        """
        :return:
        """
        if not self.es.indices.exists(index=self._index):
            self.es.indices.create(self._index, body=dict(
                settings=self.settings, mappings=self.mappings))
        self.es.indices.put_mapping(index=self._index, body=self.mappings)

    def save(self, data, get_body_query_func=get_update_body_query):
        """
        index dữ liệu đơn lẻ vào elastic search
        :param data: EsData
        :param get_body_query_func: function
        :return:
        """
        _id = data.get(self.id_key)
        body = get_body_query_func(data)
        if self.es.indices.exists(index=self._index):
            res = self.es.update(index=self._index,
                                 id=_id, body=body, retry_on_conflict=5)
            return res
        else:
            raise Exception('Index not exist')

    def get(self, _id):
        return self.es.get(self._index, _id).get("_source")

    def remove_index_if_exist(self):
        if self.es.indices.exists(index=self._index):
            self.es.indices.delete(self._index)
