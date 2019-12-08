from . import es
from settings import index, NUM_HITS
from .utils import extract_result


def search(user_id, string_query):
    body = {
        "query": {
            "bool": {
                "filter": {
                    "bool": {
                        "should": [
                            {
                                "term": {
                                    "owner": user_id
                                }
                            },
                            {
                                "term": {
                                    "users_shared": user_id
                                }
                            }
                        ]
                    }
                },
                "should": [
                    {"match": {"file_title": string_query}},
                    {"match": {"description": string_query}}
                ]
            }
        }
    }
    res = es.search(index=index, body=body, size=NUM_HITS)
    return extract_result(res['hits']['hits'])


