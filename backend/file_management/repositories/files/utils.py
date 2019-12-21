from config import FILES_INDEX
from file_management.constant import pathconst


def get_role_of_user(user_id, file_id):
    from file_management.repositories.files import es
    cur_id = file_id
    viewable = False
    editable = False
    is_owner = False
    while es.exists(index=FILES_INDEX, id=cur_id):
        cur_file = es.get_source(index=FILES_INDEX, id=cur_id)
        if (cur_file['owner'] == user_id):
            is_owner = True
        if cur_file['share_mode'] == 1 and user_id in cur_file['children_id']:
            viewable = True
            if cur_file['editable'] == True:
                editable = True
        if cur_file['share_mode'] == 2:
            viewable = True
        if is_owner: break
        cur_id = cur_file['parent_id']
    if is_owner:
        viewable = True
        editable = True
    return {
        'is_owner': is_owner,
        'viewable': viewable,
        'editable': editable
    }


def get_ancestors(file_id):
    from file_management.repositories.files import es
    ancestors = []
    cur_id = file_id
    while es.exists(index=FILES_INDEX, id=cur_id):
        ancestors.append(cur_id)
        cur_id = es.get_source(index=FILES_INDEX, id=cur_id)['parent_id']
    ancestors.append(cur_id)
    ancestors.append(pathconst.FAKE_HDD)
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
    from file_management.repositories.files import es
    children = es.get_source(index=FILES_INDEX, id=file_id)['children_id']
    descendants += children
    for child in children:
        descendants += get_descendants(child)
    return descendants


def get_file(file_id):
    from file_management.repositories.files import es
    if es.exists(index=FILES_INDEX, id=file_id):
        return es.get_source(index=FILES_INDEX, id=file_id)
    else:
        return None


def is_this_file_exists(file_id):
    from file_management.repositories.files import es
    return es.exists(index=FILES_INDEX, id=file_id)
