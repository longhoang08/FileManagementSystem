from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from file_management.extensions.custom_exception import PermissionException, UserNotFoundException
from file_management import models
from file_management.repositories.files.utils import get_ancestors


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

def check_role(file_id, user_id):
    ancestors = get_ancestors(file_id)
