from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from file_management.extensions.custom_exception import PermissionException, UserNotFoundException, FileDeletedException
from file_management import models
from file_management.repositories.files.utils import get_ancestors, get_role_of_user, get_role_of_user_not_trashed
from file_management.repositories.user import find_one_by_email


def get_email_in_jwt():
    try:
        verify_jwt_in_request()
        email = get_jwt_identity()
        return email
    except Exception as e:
        return None


def user_required(fn):
    """
    Check user role,
    if not, throw Exception
    """

    @wraps(fn)
    def wrapper(*arg, **kwargs):
        verify_jwt_in_request()
        email = get_jwt_identity()
        if email is None:
            raise PermissionException("Login required")
        return fn(*arg, **kwargs)

    return wrapper


def admin_required(fn):
    """
    Check admin role,
    if not, throw Exception
    """

    @wraps(fn)
    def wrapper(*arg, **kwargs):
        verify_jwt_in_request()
        email = get_jwt_identity()
        if email is None:
            raise PermissionException()
        user = models.User.query.filter_by(email=email).first()
        if user is None:
            raise UserNotFoundException()
        if not user.is_admin:
            raise PermissionException("Admin required")
        return fn(*arg, **kwargs)

    return wrapper


def viewable_check(file_id, error_message='You are not allowed to view this file!'):
    email = get_email_in_jwt()
    user_id = None
    if email:
        user_id = find_one_by_email(email).id
        user_id = str(user_id) if user_id else user_id
    permission = get_role_of_user_not_trashed(user_id, file_id)
    if permission.get('trashed'):
        raise FileDeletedException()
    if not permission['viewable']:
        raise PermissionException(error_message)
    return permission, {'user_id': user_id, 'email': email}


def view_privilege_required(fn):
    """
    Check if a user is allowed to view this file
    """

    @wraps(fn)
    def wrapper(*args, file_id, **kwargs):
        verify_jwt_in_request()
        email = get_jwt_identity()
        if email is None:
            raise PermissionException()
        user = models.User.query.filter_by(email=email).first()
        if user is None:
            raise UserNotFoundException()
        user_permission = get_role_of_user(user_id=user.id, file_id=file_id)
        if user_permission['is_owner'] or user_permission['editable'] or user_permission['viewable']:
            return fn(*args, file_id, **kwargs)
        else:
            raise PermissionException('You are not allowed to view this file!')

    return wrapper


def edit_privilege_required(fn):
    """
    Check if a user is allowed to edit this file
    """

    @wraps(fn)
    def wrapper(file_id, **kwargs):
        verify_jwt_in_request()
        email = get_jwt_identity()
        if email is None:
            raise PermissionException()
        user = models.User.query.filter_by(email=email).first()
        if user is None:
            raise UserNotFoundException()
        user_permission = get_role_of_user(user_id=user.id, file_id=file_id)
        if user_permission['is_owner'] or user_permission['editable']:
            return fn(file_id, **kwargs)
        else:
            raise PermissionException('You are not allowed to edit this file!')

    return wrapper


def owner_privilege_required(fn):
    """
    Check if a user is allowed to edit this file
    """

    @wraps(fn)
    def wrapper(file_id, **kwargs):
        verify_jwt_in_request()
        email = get_jwt_identity()
        if email is None:
            raise PermissionException()
        user = models.User.query.filter_by(email=email).first()
        if user is None:
            raise UserNotFoundException()
        user_permission = get_role_of_user(user_id=user.id, file_id=file_id)
        if user_permission['is_owner']:
            return fn(file_id, **kwargs)
        else:
            raise PermissionException('You must be owner to authorize!')

    return wrapper


def check_insert_privilege(user_id, parent_id):
    privileges = get_role_of_user(user_id=user_id, file_id=parent_id)
    if not (privileges['is_owner'] and privileges['editable']):
        raise PermissionException('You are not allowed to insert file into this folder')
