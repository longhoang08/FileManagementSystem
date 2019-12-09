from . import es
from config import FILES_INDEX


def get_ancestors(file_id):
    ancestors = []
    cur_id = file_id
    while es.exists(index=FILES_INDEX, id=cur_id):
        ancestors.append(cur_id)
        cur_id = es.get_source(index=FILES_INDEX, id=cur_id)['parent_id']
    ancestors.append(cur_id)
    return ancestors[::-1]


def extract_result(response, has_string_query=True):
    results = []
    for doc in response:
        if has_string_query and doc['_score'] > 0:
            results.append(doc['_source'])
        if not has_string_query:
            results.append(doc['_source'])
    return results


def get_descendants(file_id):
    descendants = []
    children = es.get_source(index=FILES_INDEX, id=file_id)['children_id']
    descendants += children
    for child in children:
        descendants += get_descendants(child)
    return descendants
