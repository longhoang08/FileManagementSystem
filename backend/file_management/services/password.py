from file_management import repositories
from file_management.extensions.custom_exception import UserNotFoundException, PasswordDiffException, \
    WrongCurrentPasswordException
from file_management.helpers import verify_password
from file_management.repositories.password import find_all_password_by_userid


def is_this_password_valid(user_id, new_password):
    passwords = find_all_password_by_userid(user_id)
    for store_password in passwords:
        if (verify_password(store_password.password, new_password)):
            return False
    return True


# you need to change password of user and add new password to historic password
def set_new_password(user, new_password):
    user_id = user.id
    repositories.user.change_password(user, new_password)
    repositories.password.add_new_password_to_database(user_id, new_password)
    return user


def change_password(email, current_password, new_password, **kwargs):
    user = repositories.user.find_one_by_email(email)
    if not user:
        raise UserNotFoundException()
    if not verify_password(user.password, current_password):
        raise WrongCurrentPasswordException()
    user_id = user.id
    if (is_this_password_valid(user_id, new_password)):
        set_new_password(user, new_password)
        return user
    else:
        raise PasswordDiffException()
