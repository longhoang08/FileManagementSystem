# coding=utf-8
import logging
import shutil
import os
from flask_jwt_extended import get_jwt_identity

from file_management import services
from file_management.helpers.check_role import check_insert_privilege, viewable_check
from file_management.extensions.custom_exception import UserNotFoundException, DiffParentException, \
    FileNotExistException, PermissionException
from file_management.helpers.check_role import user_required, owner_privilege_required, get_email_in_jwt, \
    edit_privilege_required
from file_management.helpers.transformer import add_user_name_to_files, extract_file_data_from_response
from file_management.repositories.files import FileElasticRepo, utils
from file_management.repositories.files import update
from file_management.repositories import files
from file_management.helpers.upload import generate_file_id

__author__ = 'LongHB'

from file_management.repositories.files.utils import get_file, get_role_of_user, get_descendants_of_list

from file_management.repositories.user import find_one_by_email
from file_management.services.folder import create_folder
from file_management.services.upload import check_duplicate

_logger = logging.getLogger(__name__)


def search(args):
    email = get_email_in_jwt()
    if email:
        args['user_id'] = find_one_by_email(email).id
        if args.get('user_id'):
            args['user_id'] = str(args['user_id'])
    file_id = args.get('file_id')
    if file_id:
        if isinstance(file_id, list):
            for id in file_id:
                viewable_check(id, error_message="You are not allowed to view this file/folder")
        else:
            viewable_check(file_id, error_message="You are not allowed to view this file/folder")

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
        return update.update(file_id, share_mode=share_mode, users_shared=[]).get('result')  # private
    elif args.get('emails'):
        share_mode = 1
        users_shared = []
        for email in args['emails']:
            user_shared = find_one_by_email(email)
            if not user_shared:
                raise UserNotFoundException("User with email " + email + " not exist!!!")
            users_shared.append(user_shared.id)
        for user_id in users_shared:
            from file_management.services.notification import create_notification
            create_notification(
                owner=int(args.get('user_id')),
                viewed=False,
                user_id=user_id,
                file_id=file.get('file_id')
            )
        users_shared = [str(id) for id in users_shared]
        return update.update(file_id, share_mode=share_mode, users_shared=users_shared).get('result')  # custom
    elif args.get('share_by_link'):
        share_mode = 2
        return update.update(file_id, share_mode=share_mode, users_shared=[]).get('result')  # public


@user_required
def move2trash(file_ids=None):
    """
    Move files to trash
    """
    email = get_email_in_jwt()
    user_id = str(find_one_by_email(email).id)

    if not isinstance(file_ids, list):
        return "Only accept `list` datatype"
    if len(file_ids) == 0:
        return "Nothing to move!"

    parent_of_first_file = files.utils.get_file(file_ids[0])
    parent_of_first_file = parent_of_first_file['parent_id']

    deleting_file = [files.utils.get_file(file_id) for file_id in file_ids]

    for file in deleting_file:
        file_id = file.get("file_id")
        if file.get('parent_id') != parent_of_first_file:
            raise DiffParentException("Can't move files which have different parents")
        user_permission = get_role_of_user(user_id=user_id, file_id=file_id)
        if not user_permission.get('is_owner'):
            raise PermissionException("You can't delete file of another user!")
        if file_id == user_id:
            raise PermissionException("You can't delete your home folder")

    for file_id in file_ids:
        move_one_file_to_trash(file_id)

    return True


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
    email = get_jwt_identity()
    user_id = find_one_by_email(email).id
    user_id = str(user_id)

    for file_id in file_ids:
        permission = get_role_of_user(user_id, file_id)
        if not permission.get('is_owner'):
            raise PermissionException("You can't delete this files since you are not their owner")
        if file_id == user_id:
            raise PermissionException("You can't delete your home folder")

    file_ids = get_descendants_of_list(file_ids)
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
    move_files = [files.utils.get_file(file_id) for file_id in file_ids]
    for file in move_files:
        if file.get('parent_id') != parent_of_first_file:
            raise DiffParentException("Can't move files which have different parents")
    for file_id in file_ids:
        move_one_file(file_id, new_parent)


@user_required
def copy_files(file_ids, new_parent):
    try:
        email = get_jwt_identity()
        user_id = find_one_by_email(email).id
    except Exception as e:
        _logger.error(e)
        raise UserNotFoundException()
    check_insert_privilege(parent_id=new_parent, user_id=user_id)

    parent_of_first_file = files.utils.get_file(file_ids[0])
    parent_of_first_file = parent_of_first_file['parent_id']
    copy_files = [files.utils.get_file(file_id) for file_id in file_ids]
    for file in copy_files:
        if file.get('parent_id') != parent_of_first_file:
            raise DiffParentException("Can't copy files which have different parents")
    for file_id in file_ids:
        copy_one_file(file_id, new_parent, user_id)


def copy_one_file(file_id, new_parent, user_id):
    file = files.utils.get_file(file_id)
    if file is None:
        return False
    # copy cung folder
    same_folder = False
    if file['parent_id'] == new_parent:
        same_folder = True

    if file['file_type'] == 'folder':
        if len(file['children_id']) > 0:
            create = create_folder(
                {'parent_id': new_parent, "file_title": check_duplicate(file['file_title'], new_parent)})
            for child in file['children_id']:
                copy_one_file(child, create["_id"], user_id)
            return True
        else:
            create = create_folder(
                {'parent_id': new_parent, "file_title": check_duplicate(file['file_title'], new_parent)})
            return True

    folders = utils.get_ancestors(str(user_id))
    old_folder_path = '/'.join(folders) + '/'
    print(old_folder_path)
    new_id = generate_file_id(user_id)
    print("new id:", new_id)
    shutil.copy(old_folder_path + file_id, old_folder_path + new_id)
    insert_new_copy_file(new_id, new_parent, file_id, same_folder)
    return True


def insert_new_copy_file(new_id, new_parent, old_id, same_folder):
    data = files.utils.get_file(old_id)
    file_title = check_duplicate(data['file_title'], new_parent)
    files.insert.insert(new_id,
                        file_title,
                        data['size'],
                        new_parent,
                        data['owner'],
                        data['file_type'],
                        data['file_tag'],
                        data['thumbnail_url'],
                        children_id=data['children_id'],
                        )


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


@user_required
def delete_all_file_in_trash():
    email = get_email_in_jwt()
    id = find_one_by_email(email).id
    response = services.file.search({
        "trash": True,
        'user_id': str(id),
        'basic_info': True,
        '_page': 1,
        '_limit': 10000
    })
    ids = [file.get('file_id') for file in response['result']['files']]
    drop_out(ids)
