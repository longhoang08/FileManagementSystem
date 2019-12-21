from config import FILES_INDEX
from .utils import get_descendants, get_ancestors
from .update import update


def delete(file_id):
    from . import es
    if not es.exists(index=FILES_INDEX, id=file_id):
        """
        If not exist, return immediately!
        """
        return True
    file = es.get_source(index=FILES_INDEX, id=file_id)
    descendants = get_descendants(file_id)
    ancestors = get_ancestors(file_id)

    if es.exists(index=FILES_INDEX, id=file['parent_id']):
        parent = es.get_source(index=FILES_INDEX, id=file['parent_id'])
        children = parent['children_id']
        try:
            children.remove(file_id)
        except:
            print('No such child!')
        update(parent['file_id'], children_id=children)

    es.indices.refresh(index=FILES_INDEX)
    es.update_by_query(
        index=FILES_INDEX,
        body={
            "query": {
                "terms": {
                    "file_id": ancestors[1:]
                }
            },
            "script": {
                "lang": "painless",
                "source": "ctx._source.size -= params.capacity",
                "params": {
                    "capacity": file['size']
                }
            }
        }
    )

    es.indices.refresh(index=FILES_INDEX)
    es.delete_by_query(
        index=FILES_INDEX,
        body={
            "query": {
                "terms": {
                    "file_id": [file_id] + descendants
                }
            }
        }
    )
    return True
