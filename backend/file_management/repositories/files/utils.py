from config import FILES_INDEX
from file_management.constant import pathconst


def get_ancestors(file_id):
    from file_management.repositories.files import es
    ancestors = []
    cur_id = file_id
    while es.exists(index=FILES_INDEX, id=cur_id):
        ancestors.append(cur_id)
        cur_id = es.get_source(index=FILES_INDEX, id=cur_id)['parent_id']
    ancestors.append(cur_id)
    ancestors.append(pathconst.FAKE_HDD)
    print(ancestors)
    print(file_id)
    print(type(file_id))
    return ancestors[::-1]


def extract_result(response, has_string_query=True):
    from file_management.repositories.files import es
    results = []
    for doc in response:
        if has_string_query and doc['_score'] > 0:
            results.append(doc['_source'])
        if not has_string_query:
            results.append(doc['_source'])
    return results


def get_descendants(file_id):
    descendants = []
    from file_management.repositories.files import es
    children = es.get_source(index=FILES_INDEX, id=file_id)['children_id']
    descendants += children
    for child in children:
        descendants += get_descendants(child)
    return descendants
