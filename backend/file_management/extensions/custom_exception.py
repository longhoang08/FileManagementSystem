# coding=utf-8
import logging

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)

from file_management.extensions.exceptions import HTTPException
from file_management.constant import message


class WrongPasswordException(HTTPException):
    def __init__(self, message=message.WRONG_PASSWORD, errors=None):
        super().__init__(code=401, message=message, errors=errors, custom_code='wrong_pass')


class WrongCurrentPasswordException(HTTPException):
    def __init__(self, message=message.WRONG_CUR_PASSWORD, errors=None):
        super().__init__(code=401, message=message, errors=errors, custom_code='wrong_cur_pass')


class PasswordDiffException(HTTPException):
    def __init__(self, message=message.PASSWORD_DIFF, errors=None):
        super().__init__(code=401, message=message, errors=errors, custom_code='pass_diff')


class BlockingException(HTTPException):
    def __init__(self, message=message.BLOCKING, errors=None):
        super().__init__(code=403, message=message, errors=errors, custom_code='blocking')


class BlockedException(HTTPException):
    def __init__(self, message=message.BLOCKED, errors=None):
        super().__init__(code=403, message=message, errors=errors, custom_code='blocked')


class PermissionException(HTTPException):
    def __init__(self, message=message.PERMISSION, errors=None):
        super().__init__(code=403, message=message, errors=errors, custom_code='permission')


class NeedLoggedInException(HTTPException):
    def __init__(self, message=message.PLEASE_LOGIN, errors=None):
        super().__init__(code=401, message=message, errors=errors, custom_code='please_login')


class InvalidLoginTokenException(HTTPException):
    def __init__(self, message=message.INVALID_LOGIN_TOKEN, errors=None):
        super().__init__(code=401, message=message, errors=errors, custom_code='invalid_login_token')


class InvalidTokenException(HTTPException):
    def __init__(self, message=message.INVALID_TOKEN, errors=None):
        super().__init__(code=401, message=message, errors=errors, custom_code='invalid_token')


class EncodeErrorException(HTTPException):
    def __init__(self, message=message.ENCODE_ERR, errors=None):
        super().__init__(code=401, message=message, errors=errors, custom_code='encode_err')


class CantSendEmailException(HTTPException):
    def __init__(self, message=message.CANT_SEND_EMAIL, errors=None):
        super().__init__(code=502, message=message, errors=errors, custom_code='mail_server_err')


class UserNotFoundException(HTTPException):
    def __init__(self, message=message.USER_NOT_FOUND, errors=None):
        super().__init__(code=400, message=message, errors=errors, custom_code='user_not_found')


class UsernameNotMatchEmailException(HTTPException):
    def __init__(self, message=message.USERNAME_NOT_MATCH_EMAIL, errors=None):
        super().__init__(code=401, message=message, errors=errors, custom_code='username_not_match_email')


class RegisterBeforeException(HTTPException):
    def __init__(self, message='registed before', errors=None):
        super().__init__(code=409, message=message, errors=errors, custom_code='registed_before')


class UserExistsException(HTTPException):
    def __init__(self, message='user exists', errors=None):
        super().__init__(code=409, message=message, errors=errors, custom_code='user_exists')


class NotRegisterdException(HTTPException):
    def __init__(self, message=message.REGISTED, errors=None):
        super().__init__(code=401, message=message, errors=errors, custom_code='not_registerd')


class MustConfirmEmailException(HTTPException):
    def __init__(self, message=message.MUST_CONFIRM_EMAIL, errors=None):
        super().__init__(code=401, message=message, errors=errors, custom_code='must_confirm')


class NotInPendingException(HTTPException):
    def __init__(self, message=message.NOT_IN_PENDING, errors=None):
        super().__init__(code=401, message=message, errors=errors, custom_code='not_pending')


class InvalidGoogleTokenException(HTTPException):
    def __init__(self, message=message.INVALID_GOOGLE_TOKEN, errors=None):
        super().__init__(code=401, message=message, errors=errors, custom_code='invalid_google_token')


class CannotUploadFileException(HTTPException):
    def __init__(self, message=message.CANT_UPLOAD_AVATAR, errors=None):
        super().__init__(code=400, message=message, errors=errors, custom_code='can_not_upload')


class PathUploadNotFound(HTTPException):
    def __init__(self, message=message.CANT_UPLOAD_FILE, errors=None):
        super().__init__(code=400, message=message, errors=errors, custom_code='can_not_upload_file')


class CannotDownloadFile(HTTPException):
    def __init__(self, message=message.CANT_DOWNLOAD_FILE, errors=None):
        super().__init__(code=400, message=message, errors=errors, custom_code='can_not_download_file')


class DiffParentException(HTTPException):
    def __init__(self, message=message.PARENT_DIFF, errors=None):
        super().__init__(code=400, message=message, errors=errors, custom_code='can_not_move_files_to_trash')


class FileNotExistException(HTTPException):
    def __init__(self, message="File/folder not exists", errors=None):
        super().__init__(code=400, message=message, errors=errors, custom_code='file_not_exist')
