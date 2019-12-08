from . import es
from settings import index


def update(file_id, **kwargs):
    update_body = {}
    fields = ['file_title', 'file_type', 'owner', 'star', 'parent_id', 'share_mode', 'editable', 'users_shared',
              'children_id', 'size', 'description', 'file_tag', 'created_at', 'updated_at']
    file = es.get_source(index=index, id=file_id)
    
    for field in fields:
        if field in kwargs:
            new_value = kwargs.get(field)
            old_value = file[field]

            if isinstance(new_value, list):
                new_value.sort()
                old_value.sort()

            if new_value != old_value:
                update_body[field] = new_value

    es.indices.refresh(index=index)
    res = es.update(
        index=index,
        id=file_id,
        body={
            "doc": update_body
        }
    )
    return res