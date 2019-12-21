from config import FILES_INDEX
from .utils import get_ancestors


def update(file_id, **kwargs):
    update_body = {}
    fields = ['file_title', 'file_type', 'owner', 'star', 'parent_id', 'share_mode', 'editable', 'users_shared',
              'children_id', 'size', 'description', 'file_tag', 'created_at', 'updated_at']
    from file_management.repositories.files import es
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
                    update_size(old_value, new_value, file['size'])

                update_body[field] = new_value

    es.indices.refresh(index=FILES_INDEX)
    res = es.update(
        index=FILES_INDEX,
        id=file_id,
        body={
            "doc": update_body
        }
    )
    return res


def update_size(old_parent, new_parent, file_size):
    """
    This Method should not be called directly
    :param old_parent: Old Parent
    :param new_parent: New Parent
    :param file_size: File Size
    :return: Something amazing!
    """
    old_ancestors = set(get_ancestors(old_parent))
    new_ancestors = set(get_ancestors(new_parent))

    negotiate_size = list(old_ancestors.difference(new_ancestors))
    advance_size = list(new_ancestors.difference(old_ancestors))

    from file_management.repositories.files import es
    es.indices.refresh(index=FILES_INDEX)
    es.update_by_query(
        index=FILES_INDEX,
        body={
            "query": {
                "terms": {
                    "file_id": negotiate_size
                }
            },
            "script": {
                "lang": "painless",
                "source": "ctx._source.size += params.capacity",
                "params": {
                    "capacity": -1 * file_size
                }
            }
        }
    )

    es.indices.refresh(index=FILES_INDEX)
    es.update_by_query(
        index=FILES_INDEX,
        body={
            "query": {
                "terms": {
                    "file_id": advance_size
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

def update_share(file_id, users_shared = [], share_mode = 0, **kwargs):
    return update(file_id, users_shared, share_mode, **kwargs)