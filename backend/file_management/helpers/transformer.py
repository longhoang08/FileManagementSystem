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


def extract_file_data_from_response(responses):
    if not responses:
        return {'result': {'files': []}}
    responses = responses.to_dict()
    hits = responses['hits']['hits']
    files = [item['_source'] for item in hits]
    return {'result': {'files': files}}


def format_details_args(args: dict):
    if not args: args = {}
    if not args.get('_limit'):
        args['_limit'] = 12
    if not args.get('_page'):
        args['_page'] = 1
