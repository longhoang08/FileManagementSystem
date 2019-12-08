from . import es
from file_management.models.file import NUM_HITS
from config import FILES_INDEX
from .utils import extract_result


def search(user_id, string_query=None):
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
                "should": []
            }
        }
    }
    if string_query is not None:
        body["query"]["bool"]["should"] = [
            {"match": {"file_title": string_query}},
            {"match": {"description": string_query}}
        ]
    res = es.search(index=FILES_INDEX, body=body, size=NUM_HITS)

    return extract_result(res['hits']['hits'], (string_query is not None))

