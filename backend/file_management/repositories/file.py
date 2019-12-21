# coding=utf-8
import json
import logging

from elasticsearch_dsl import query, Search

from config import FILES_INDEX
from file_management import BadRequestException
from file_management.models.file import mappings, settings
from file_management.repositories.es_base import EsRepositoryInterface

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)

FOLDER_DETAILS = ["star", "owner", "editable", "created_at", "description", "children_id"]


class FileElasticRepo(EsRepositoryInterface):
    def __init__(self):
        super().__init__()
        self._index = FILES_INDEX
        self.mappings = mappings
        self.settings = settings
        self.id_key = 'file_id'

    def search(self, args):
        """
        exec query and return response
        :param args:
        :return:
        """
        file_es = self.build_file_query(args)
        # print(json.dumps(file_es.to_dict()))
        responses = file_es.using(self.es).index(self._index).execute()
        return responses

    def get_must_conditions(self, args):
        conditions = []
        file_id = args.get('file_id')
        if file_id:
            if isinstance(file_id, list):
                conditions.append(query.Terms(file_id=file_id))
            else:
                conditions.append(query.Term(file_id=file_id))
        search_text = args.get('q')
        if search_text:
            conditions.append(query.DisMax(queries=[
                query.MatchPhrasePrefix(file_title={
                    'query': search_text,
                    'boost': 10
                }),
                query.Match(file_title={
                    'query': search_text,
                    'boost': 4,
                    'operator': 'and'
                }),
                query.Match(description={
                    'query': search_text,
                    'boost': 1,
                    'operator': 'or'
                })
            ]))
        if not conditions:
            conditions.append(query.MatchAll())
        return conditions

    def build_filter_condions(self, args):
        if not args.get('user_id'):
            raise BadRequestException("Required user id in arguments")
        must_conditions = []
        must_conditions.append(query.Term(owner=args.get('user_id')))
        must_conditions.append(query.Bool(
            should=[
                query.Term(trashed=False),
                query.Bool(must_not=query.Exists(field="trashed"))
            ] if not args.get('trash') else [query.Term(trashed=True)]
        ))
        if args.get('star'):
            must_conditions.append(query.Term(star=True))
        if args.get('only_photo'):
            must_conditions.append(query.Prefix(file_type={'value': 'image'}))

        return query.Bool(must=must_conditions)

    def get_children_of_folder(self, folder_id):
        try:
            response = self.es.get(self._index, folder_id, _source=FOLDER_DETAILS)['_source']
            return response
        except Exception as e:
            _logger.error(e)
            raise BadRequestException('Folder not exist')

    def build_file_query(self, args):
        """
        Build query for es
        :param args:
        :return:
        """
        conditions = query.Bool(
            must=self.get_must_conditions(args),
            filter=[self.build_filter_condions(args)]
        )
        file_es = self.build_file_es(args, conditions)
        print(json.dumps(file_es.to_dict()))
        return file_es

    def build_file_es(self, args, search_condition):
        file_es = Search() \
            .query(search_condition)
        file_es = file_es.sort(*self.sort_condition(args))
        file_es = self.add_custom_source(file_es, args)
        file_es = self.add_page_limit_to_file_es(args, file_es)
        return file_es

    def add_custom_source(self, file_es, args):
        sources = []
        if (args.get('get_children_id')):
            sources += ['children_id']
        if (args.get('basic_info')):
            sources += ['file_title', 'star', 'updated_at', 'file_type', 'file_id']
        if sources:
            file_es = file_es.source(sources)
        return file_es

    def add_page_limit_to_file_es(self, args, file_es):
        _page = args.get('_page') if args.get('_page') else 1
        _limit = args.get('_limit') if args.get('_limit') else 12
        file_es = file_es[(_page - 1) * _limit: _page * _limit]
        return file_es

    def sort_condition(self, args):
        sort_conditions = [self.sort_by_score(), self.sort_by_time()]
        if args.get('q'):
            return sort_conditions
        else:
            return sort_conditions[::-1]

    def sort_by_score(self):
        return {
            '_score': {
                'order': 'desc'
            }
        }

    def sort_by_time(self):
        return {
            'updated_at': {
                'order': 'desc'
            }
        }

    def get_permission(self, user_id, file_ids):
        query_conditions = query.Bool(must=[
            query.Terms(file_id=file_ids),
            query.Bool(should=[
                query.Term(owner={
                    'value': user_id,
                    'boost': 100
                }),
                query.Bool(must=[
                    query.Term(share_mode={
                        'value': 1,
                        'boost': 5
                    }),
                    query.Term(users_shared={
                        'value': user_id,
                        'boost': 5
                    })
                ]),
                query.Term(share_mode=2)
            ])
        ])
        file_es = Search() \
            .query(query_conditions) \
            .source(['owner', 'share_mode', 'editable'])
        file_es = file_es[0:1]
        print(json.dumps(file_es.to_dict()))
        responses = file_es.using(self.es).index(self._index).execute()
        return responses
