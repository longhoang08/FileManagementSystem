# coding=utf-8
import logging

from flask_jwt_extended import get_jwt_identity

from file_management.helpers.check_role import check_insert_privilege
from file_management.extensions.custom_exception import UserNotFoundException, DiffParentException, \
    FileNotExistException, PermissionException
from file_management.helpers.check_role import user_required, owner_privilege_required, get_email_in_jwt, \
    edit_privilege_required
from file_management.helpers.transformer import add_user_name_to_files, extract_file_data_from_response
from file_management.repositories.files import FileElasticRepo
from file_management.repositories.files import update
from file_management.repositories import files

__author__ = 'LongHB'

from file_management.repositories.files.utils import get_file

from file_management.repositories.user import find_one_by_email

_logger = logging.getLogger(__name__)


def search(args):
    email = get_email_in_jwt()
    if email:
        args['user_id'] = find_one_by_email(email).id
        if args.get('user_id'):
            args['user_id'] = str(args['user_id'])
    file_es = FileElasticRepo()
    response = file_es.search(args)
    response = extract_file_data_from_response(response)
    add_user_name_to_files(response['result']['files'])
    return response


@user_required
def share(args):
    try:
        email = get_jwt_identity()
        args['user_id'] = str(find_one_by_email(email).id)
    except Exception as e:
        _logger.error(e)
        raise UserNotFoundException()

    file_id = args['file_id']
    file = get_file(file_id)
    if not file:
        raise FileNotExistException()
    if (file['owner'] != args['user_id']):
        raise PermissionException("You are not the owner of this file/folder")

    if args.get('private'):
        share_mode = 0
        return update.update(file_id, share_mode=share_mode).get('result')  # private
    elif args.get('emails'):
        share_mode = 1
        users_shared = [str(find_one_by_email(mail).id) for mail in args['emails']]
        return update.update(file_id, share_mode=share_mode, users_shared=users_shared).get('result')  # custom
    elif args.get('share_by_link'):
        share_mode = 2
        return update.update(file_id, share_mode=share_mode).get('result')  # public


def move2trash(file_ids=None):
    """
    Move files to trash
    """
    if not isinstance(file_ids, list):
        return "Only accept `list` datatype"
    if len(file_ids) == 0:
        return "Nothing to move!"

    parent_of_first_file = files.utils.get_file(file_ids[0])
    parent_of_first_file = parent_of_first_file['parent_id']
    for file_id in file_ids:
        parent_id = files.utils.get_file(file_ids[0])['parent_id']
        if parent_id != parent_of_first_file:
            """
            All file must have same parent_id, else throws Exception
            """
            raise DiffParentException()
        move_one_file_to_trash(file_id)
    return True


@owner_privilege_required
def move_one_file_to_trash(file_id):
    files.update.update(file_id, trashed=True)


@user_required
def restore_files(file_ids=None):
    """
    Restore files from trash
    """
    if not file_ids:
        return "Nothing to restore!"
    for file_id in file_ids:
        file = files.utils.get_file(file_id)
        if not file['trashed']:
            continue
        parent_id = file['parent_id']
        parent_new_children = files.utils.add_child(file_id=parent_id, child_id=file_id)
        files.update.update(parent_id, children_id=parent_new_children)
        files.update.update(file_id, trashed=False)
    return True


@user_required
def drop_out(file_ids):
    """
    Drop away files from ES
    """
    for file_id in file_ids:
        files.delete.delete(file_id)


@user_required
def add_star(file_id):
    files.update.update(file_id, star=True)


@user_required
def remove_star(file_id):
    files.update.update(file_id, star=False)


@user_required
def move_files(file_ids, new_parent):
    try:
        email = get_jwt_identity()
        user_id = find_one_by_email(email).id
    except Exception as e:
        _logger.error(e)
        raise UserNotFoundException()
    check_insert_privilege(parent_id=new_parent, user_id=user_id)
    parent_of_first_file = files.utils.get_file(file_ids[0])
    parent_of_first_file = parent_of_first_file['parent_id']
    for file_id in file_ids:
        parent_id = files.utils.get_file(file_ids[0])['parent_id']
        if parent_id != parent_of_first_file:
            """
            All file must have same parent_id, else throws Exception
            """
            raise DiffParentException()
        move_one_file(file_id, new_parent)


def move_one_file(file_id, new_parent):
    file = files.utils.get_file(file_id)
    if file is None:
        """
        File đếch tồn tại thì move làm mẹ gì bạn!
        """
        return True
    old_parent_new_children = files.utils.remove_child(file_id=file['parent_id'], child_id=file_id)
    new_parent_new_children = files.utils.add_child(file_id=new_parent, child_id=file_id)

    files.update.update(file['parent_id'], children_id=old_parent_new_children)  # Update old parent
    files.update.update(new_parent, children_id=new_parent_new_children)  # Update new parent
    files.update.update(file_id, parent_id=new_parent)  # Update itself
    return True


@edit_privilege_required
def rename_file(file_id, new_name):
    files.update.update(file_id, file_title=new_name)
