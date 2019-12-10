from . import es
from config import FILES_INDEX
from .utils import get_ancestors
from .update import update


def insert(file_id, file_title, file_size, parent_id, user_id, mime_type, tags, starred=False, created_at=None,
           updated_at=None):
    document = {
        "file_id": file_id,
        "file_title": file_title,
        "size": file_size,
        "file_type": mime_type,
        "owner": user_id,
        "star": starred,
        "parent_id": parent_id,
        "children_id": [],
        "share_mode": 0,
        "editable": False,
        "users_shared": [],
        "created_at": created_at,
        "updated_at": updated_at,
        "file_tag": tags,
        "description": ""
    }

    res = es.index(index=FILES_INDEX, body=document, id=file_id)
    ancestors = get_ancestors(parent_id)

    if es.exists(index=FILES_INDEX, id=parent_id):
        parent = es.get_source(index=FILES_INDEX, id=parent_id)
        update(file_id=parent_id, children_id=parent['children_id'] + [file_id])

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
                "source": "ctx._source.size += params.capacity",
                "params": {
                    "capacity": file_size
                }
            }
        }
    )
    return res
