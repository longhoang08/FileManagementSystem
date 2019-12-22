from config import FILES_INDEX
from .utils import get_ancestors


def update(file_id, **kwargs):
    from datetime import datetime
    update_body = {}
    fields = ['file_title', 'star', 'parent_id', 'share_mode', 'editable', 'users_shared',
              'children_id', 'description', 'file_tag', 'trashed']
    from file_management.repositories.files import es
    if not es.exists(index=FILES_INDEX, id=file_id):
        return True
    file = es.get_source(index=FILES_INDEX, id=file_id)
    for field in fields:
        if field in kwargs:
            new_value = kwargs.get(field)
            old_value = file[field]

            if isinstance(new_value, list):
                new_value.sort()
                old_value.sort()

            if new_value != old_value:
                if field == 'parent_id':
                    """
                    If file is moved (i.e: changed parend_id), update size of old ancestors and new ancestors
                    """
                    old_ancestors = set(get_ancestors(old_value))
                    new_ancestors = set(get_ancestors(new_value))
                    negotiate_size = list(old_ancestors.difference(new_value))
                    advance_size = list(new_ancestors.difference(old_value))

                    update_size(negotiate_size, -1 * file['size'])  # Update old ancestors
                    update_size(advance_size, file['size'])  # Update new ancestors
                if field == 'trashed':
                    """
                    This file is moved/restored to/from trash, update size for it's ancestors
                    """
                    ancestors = get_ancestors(file['parent_id'])
                    sign = -1 if new_value else 1
                    update_body[field] = datetime.now()
                    update_size(ancestors, sign * file['size'])
                update_body[field] = new_value
                update_body['updated_at'] = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
    es.indices.refresh(index=FILES_INDEX)
    res = es.update(
        index=FILES_INDEX,
        id=file_id,
        body={"doc": update_body}
    )
    return res


def update_size(files_id, file_size):
    """
    Do not call this method directly
    """
    from file_management.repositories.files import es
    es.indices.refresh(index=FILES_INDEX)
    es.update_by_query(
        index=FILES_INDEX,
        body={
            "query": {
                "terms": {
                    "file_id": files_id
                }
            },
            "script": {
                "lang": "painless",
                "source": "ctx._source.size += params.capacity",
                "params": {
                    "capacity": file_size
                }
            }
        }
    )
