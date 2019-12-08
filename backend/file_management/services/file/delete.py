from . import es
from settings import index
from search_engine.utils import get_descendants, get_ancestors
from search_engine.update import update


def delete(file_id):
    file = es.get_source(index=index, id=file_id)
    descendants = get_descendants(file_id)
    ancestors = get_ancestors(file_id)

    if es.exists(index=index, id=file['parent_id']):
        parent = es.get_source(index=index, id=file['parent_id'])
        children = parent['children_id']
        try:
            children.remove(file_id)
        except:
            print('No such child!')
        update(parent['file_id'], children_id=children)

    es.indices.refresh(index=index)
    es.update_by_query(
        index=index,
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

    es.indices.refresh(index=index)
    es.delete_by_query(
        index=index,
        body={
            "query": {
                "terms": {
                    "file_id": [file_id] + descendants
                }
            }
        }
    )
    return True
