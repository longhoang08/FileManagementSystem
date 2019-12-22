from file_management.extensions.custom_exception import OwnerNotFoundException
from file_management.services.user import get_user_name_by_user_id


def add_user_name_to_files(files):
    for file in files:
        add_user_name_to_file(file)


def add_user_name_to_file(file):
    owner_id = file.get('owner')
    if not owner_id:
        raise OwnerNotFoundException()
    file['owner'] = {
        'id': owner_id,
        'fullname': get_user_name_by_user_id(owner_id)
    }